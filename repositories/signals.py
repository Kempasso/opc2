from dataclasses import dataclass
from sqlalchemy import select

from repositories.base import BaseRepo
from repositories.mixins import (
    CreateMixin,
    UpdateMixin,
    RetrieveMixin,
    FilterMixin,
    AsyncSession
)
from tables import Signal, Device


@dataclass
class SignalsRepo(BaseRepo, CreateMixin, UpdateMixin, RetrieveMixin, FilterMixin):
    table = Signal

    async def filter_signal_by_code_id(self, code_id: int):
        async with self.session_maker() as session:
            session: AsyncSession
            query = select(self.table).filter(self.table.code_id == code_id)
            result = await session.execute(query)
            return result.scalar()

    async def filter_codes_by_device_id_and_active_signals(self, device_id: int):
        query = select(self.table) \
            .join(Device) \
            .filter(Device.id == device_id, Signal.active)
        return query
