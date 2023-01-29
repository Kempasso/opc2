from dataclasses import dataclass

from repositories import (
    SignalsRepo,
    SignalsLogRepo,
    signals_log_repo,
    signals_repo,
)


class SignalsParser:
    @classmethod
    async def parse_row(cls, data: str):
        raise NotImplemented


@dataclass
class SignalsService:
    repository: SignalsRepo = signals_repo

    async def parse_signal(self, **kwargs):
        """
        Парсит сигнал, приходящий с устройства
        """
        # TODO: Здесь необходимо описать парсер с последующим укладыванием в базу
        await SignalsParser.parse_row(**kwargs)

    async def get_active_signals_by_device_id(self, id: int):
        """
        Позволяет получить активные сигналы для устройства
        """
        codes = await self.repository.filter_codes_by_device_id_and_active_signals(device_id=id)
        return codes

    async def get_signal_by_code_id(self, id: int):
        signal = await self.repository.filter_signal_by_code_id(code_id=id)
        return signal

    async def get_all_signals(self):
        return await self.repository.all()


@dataclass
class SignalsLogService:
    repository: SignalsLogRepo = signals_log_repo

    async def filter_log_entries_by_signal_id(self, id: int):
        query = await self.repository.do_filter(as_query=True,
                                                signal_id=id)
        return query

    async def get_all_log_entries(self):
        return await self.repository.all()
