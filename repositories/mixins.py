import typing
from dataclasses import dataclass
from datetime import datetime
from fastapi_pagination import Params
from fastapi_pagination.ext.async_sqlalchemy import paginate

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker


@dataclass
class BaseMixin:
    table: typing.Any
    engine: AsyncEngine
    session_maker: sessionmaker


@dataclass
class CreateMixin(BaseMixin):
    async def create(self, **kwargs):
        async with self.session_maker() as session:
            kwargs["created_at"] = datetime.now()
            new_obj = self.table(**kwargs)
            session.add(new_obj)
            await session.commit()
            await session.refresh(new_obj)
        return new_obj


@dataclass
class UpdateMixin(BaseMixin):
    async def update(
        self, filter_by_values: typing.Dict[str, typing.Any], new_values: dict
    ):

        async with self.session_maker() as session:
            sql_expr_filter = []
            for filter_key, val in filter_by_values.items():
                sql_expr_filter.append(getattr(self.table, filter_key) == val)

            new_values["updated_at"] = datetime.now()
            update_query = (
                update(self.table)
                .where(*sql_expr_filter)
                .values(**new_values)
                .execution_options(syncronize_session="fetch")
            )

            await session.execute(update_query)
            await session.commit()


@dataclass
class RetrieveMixin(BaseMixin):
    async def get_by_id(self, id):
        async with self.session_maker() as session:
            session: AsyncSession
            result = await session.get(self.table, id)
            return result

    async def get(self, **kwargs):
        async with self.session_maker() as session:
            session: AsyncSession
            query = select(self.table).filter_by(**kwargs)
            result = await session.execute(query)
            return result.scalar()

    async def all(self, is_query: bool = True, limit: int | None = None):
        query = select(self.table)
        if is_query:
            return query
        else:
            if limit:
                query = query.limit(limit)
            async with self.session_maker() as session:
                result = await session.execute(query)
                return result.scalars()


@dataclass
class FilterMixin(BaseMixin):
    async def do_filter(self, as_query: bool = False, **kwargs):
        query = select(self.table).filter_by(**kwargs)

        if as_query:
            return query

        async with self.session_maker() as session:
            result = await session.execute(query)
            return result.scalars()
