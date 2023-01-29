from typing import AsyncIterator
from repositories import session_maker, AsyncSession


async def get_session() -> AsyncIterator[AsyncSession]:
    async with session_maker() as session:
        yield session


from .devices import router as DeviceRouter
from .signals import router as SignalRouter
from .codes import router as CodesRouter
