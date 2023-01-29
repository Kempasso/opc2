from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.base import BaseRepo
from repositories.mixins import CreateMixin, UpdateMixin, RetrieveMixin, FilterMixin
from tables import SignalsLog, Signal


@dataclass
class SignalsLogRepo(BaseRepo, CreateMixin, UpdateMixin, RetrieveMixin, FilterMixin):
    table = SignalsLog

    async def filter_signals_by_device_id(self, device_id: int):
        async with self.session_maker() as session:
            session: AsyncSession
            query = select(self.table).join(Signal).filter(Signal.device_id == device_id)
            result = await session.execute(query)
            return result.scalars()
