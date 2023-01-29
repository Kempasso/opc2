from dataclasses import dataclass

from repositories import SignalsLogRepo, signals_log_repo


@dataclass
class SignalsLogService:
    repository: SignalsLogRepo = signals_log_repo

    async def filter_log_entries_by_signal_id(self, id: int):
        query = await self.repository.do_filter(as_query=True,
                                                signal_id=id)
        return query

    async def get_all_log_entries(self):
        return await self.repository.all()
