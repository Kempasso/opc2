import re
from datetime import datetime
from typing import Any
from dataclasses import dataclass

from repositories import (
    SignalsRepo,
    signals_repo,
)


@dataclass
class SignalsService:
    repository: SignalsRepo = signals_repo

    async def get_active_signals_by_device_id(self, id: int):
        """
        Позволяет получить активные сигналы для устройства
        """
        codes = await self.repository.filter_codes_by_device_id_and_active_signals(device_id=id)
        return codes

    async def get_signal_by_code_id(self, id: int):
        signal = await self.repository.filter_signal_by_code_id(code_id=id)
        return signal

    async def get_signals_by_device_id(self, id: int):
        signal = await self.repository.do_filter(device_id=id, as_query=True)
        return signal

    async def get_all_signals(self):
        return await self.repository.all()
