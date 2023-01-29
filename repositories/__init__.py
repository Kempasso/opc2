import datetime
import enum
import pathlib
import random
import string
import typing
from dataclasses import dataclass, field

from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    create_async_engine)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

import settings


engine: AsyncEngine = create_async_engine(settings.DB_URL, poolclass=NullPool)
session_maker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Main app repo imports
from .codes import CodesRepo
from .devices import DevicesRepo
from .signals import SignalsRepo, SignalsLogRepo

from tables import BaseModel


# Main app repo's
codes_repo = CodesRepo(engine=engine, session_maker=session_maker)
devices_repo = DevicesRepo(engine=engine, session_maker=session_maker)
signals_repo = SignalsRepo(engine=engine, session_maker=session_maker)
signals_log_repo = SignalsLogRepo(engine=engine, session_maker=session_maker)


async def create_tables():
    """
    создаёт все таблицы проекта
    """
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)


async def refresh(obj):
    async with session_maker() as sess:
        sess.add(obj)
        await sess.refresh(obj)

def string_generator(max_size=10) -> str:
    return "".join(
        random.choice(string.ascii_letters) for i in range(random.randint(0, max_size))
    )


def int_generator():
    return random.randint(0, 10000)


def float_generator():
    return random.uniform(0, 10000)


def date_generator():
    ...


def binary_generate():
    test_schema_path = pathlib.Path.cwd() / "example_data" / "new_generator.yaml"
    return test_schema_path.read_bytes()


def enum_generator(enum_clas: enum.EnumMeta):
    new_val = random.choice([el for el in enum_clas])
    return new_val


def boolean_generator():
    return random.choice([True, False])


@dataclass
class Fabric:
    #  таблица для которой будет идти генерация инстанса
    table: typing.Any
    child_fabrics: typing.Dict[str, "Fabric"] = field(default_factory=dict)
    ignore_fields: list = field(default_factory=list)
    many: bool = False

    SQLALCHEMY_TYPE_MAPPING = {
        "Text": string_generator,
        "String": string_generator,
        "Unicode": string_generator,
        "Integer": int_generator,
        "Float": float_generator,
        "DateTime": datetime.datetime.now,
        "DATETIME": datetime.datetime.now,
        "LargeBinary": binary_generate,
        "BLOB": binary_generate,
        "Password": string_generator,
        'Enum': enum_generator,
        "Boolean": boolean_generator,
    }

    def __post_init__(self):
        self.ignore_fields.append("id")

    @property
    def _table_cols(self) -> typing.Dict[str, typing.Any]:
        columns = {}
        for var_name, instance in dict(vars(self.table)).items():
            if (
                str(type(instance))
                == "<class 'sqlalchemy.orm.attributes.InstrumentedAttribute'>"
            ):
                columns.update({var_name: instance})
        return columns

    async def generate(self):
        async with session_maker() as sess:
            relationship_fields: typing.Dict[str, typing.Any] = {}
            for name, fabric in self.child_fabrics.items():
                if fabric.many:
                    related_obj = [fabric.generate_obj() for i in range(random.randint(0, 10))]
                    sess.add_all(related_obj)
                    await sess.commit()
                    [await sess.refresh(obj) for obj in related_obj]

                else:
                    related_obj = fabric.generate_obj()
                    sess.add(related_obj)
                    await sess.commit()
                    await sess.refresh(related_obj)
                relationship_fields.update({name: related_obj})

            obj = self.generate_obj(**relationship_fields)
            sess.add(obj)
            await sess.commit()
            await sess.refresh(obj)
            return obj

    def generate_obj(self, **related_objects):
        constructor_data: dict = {}
        for name, column in self._table_cols.items():
            if "ForeignKey" in repr(column.expression) or name in self.ignore_fields:
                continue
            if hasattr(column.type, "enum_class"):
                generator_instance = self.SQLALCHEMY_TYPE_MAPPING["Enum"]
                constructor_data.update({name: generator_instance(column.type.enum_class)})
            else:
                try:
                    col_type = column.type
                    generator_instance = self.SQLALCHEMY_TYPE_MAPPING[
                        repr(col_type).split("(")[0]
                    ]
                    constructor_data.update({name: generator_instance()})

                except AttributeError:
                    if name in self.child_fabrics:
                        related_object = related_objects[name]
                        constructor_data.update({name: related_object})
                    else:
                        raise Exception("какая-то пизда, пацаны")

        return self.table(**constructor_data)