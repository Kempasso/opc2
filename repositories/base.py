import typing
from dataclasses import dataclass, field

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker


@dataclass
class BaseRepo:
    table: typing.Any = field(init=False)
    engine: AsyncEngine
    session_maker: sessionmaker
