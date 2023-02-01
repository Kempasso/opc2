import typing
from dataclasses import dataclass
from sqlalchemy import select, update

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

    async def update_signal(
            self, filter_by_values: typing.Dict[str, typing.Any],
            new_values: dict
    ):
        async with self.session_maker() as session:
            sql_expr_filter = []
            for filter_key, val in filter_by_values.items():
                sql_expr_filter.append(getattr(self.table, filter_key) == val)

            update_query = (
                update(self.table)
                .where(*sql_expr_filter)
                .values(**new_values)
                .execution_options(syncronize_session="fetch")
            )

            await session.execute(update_query)
            await session.commit()

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
