import re
from datetime import datetime
from typing import Any
from dataclasses import dataclass

from repositories import (
    SignalsRepo,
    signals_repo,
)
from services import device_service, signals_log_service, signals_service


class SignalsParser:
    @classmethod
    async def parse_data(cls, data: Any):
        raise NotImplemented

        device = await device_service.get(serial=data.serial)

        if "temper" in data:
            signal = await signals_service.get(
                row="temper"
            )
            await signals_service.update(
                filter_by_values=dict(
                    id=signal.id,
                    device_id=device.id
                ),
                new_values=dict(updated_at=datetime.now(), active=True)
            )
            temper_value = int(re.search(r'\d+', data).group())
            await device_service.update_device_temperature(device.id, temper_value)
            await signals_log_service.create(signal_id=signal.id)
        else:
            elements = data.data.split(',')
            for el in elements:
                signal = await SignalsService.repository.get(row=el)
                if not signal.active:
                    await SignalsService.repository.update(
                        filter_by_values=dict(
                            id=signal.id,
                            device_id=device.id
                        ),
                        new_values=dict(updated_at=datetime.now(), active=True)
                    )
                    await signals_log_service.create(signal_id=signal.id)
                else:
                    await SignalsService.repository.update(
                        filter_by_values=dict(
                            id=signal.id,
                            device_id=device.id,
                        ),
                        new_values=dict(updated_at=datetime.now())
                    )


@dataclass
class SignalsService:
    repository: SignalsRepo = signals_repo

    async def parse_signal(self, **kwargs):
        """
        Парсит сигнал, приходящий с устройства
        """
        # TODO: Здесь необходимо описать парсер с последующим укладыванием в базу
        await SignalsParser.parse_data(**kwargs)

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
