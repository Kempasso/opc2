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
from tables import Code, Device


@dataclass
class CodesRepo(BaseRepo, CreateMixin, UpdateMixin, RetrieveMixin, FilterMixin):
    table = Code

    async def filter_codes_by_device_id(self, device_id: int):
        async with self.session_maker() as session:
            session: AsyncSession
            query = select(self.table).join(Device).filter(Device.id == device_id)
            return query
            # result = await session.execute(query)
            # return result.scalars()
