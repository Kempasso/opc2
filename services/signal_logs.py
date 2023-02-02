from dataclasses import dataclass

from repositories import SignalsLogRepo, signals_log_repo
from sqlalchemy.orm import Query


@dataclass
class SignalsLogService:
    repository: SignalsLogRepo = signals_log_repo

    async def filter_log_entries_by_signal_id(self, id: int) -> Query:
        query = await self.repository.do_filter(as_query=True,
                                                signal_id=id)
        return query

    async def filter_log_entries_by_device_id(self, id: int) -> Query:
        query = await self.repository.filter_signals_by_device_id(id)
        return query

    async def get_all_log_entries(self) -> Query:
        query = await self.repository.all()
        return query
