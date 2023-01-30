import typing
from dataclasses import dataclass

from repositories import (
    DevicesRepo,
    devices_repo
)
from tables import Device


@dataclass
class DeviceService:
    repository: DevicesRepo = devices_repo

    async def get_all_devices(self) -> typing.List[Device]:
        """
        Позволяет получить все устройства
        """
        devices = await self.repository.all()
        return devices

    async def get_device_by_id(self, id: int) -> Device:
        """
        Позволяет устройство по его ID
        :param id: id устройства
        """
        device = await self.repository.get_by_id(id)
        return device

    async def update_device_temperature(self, device_id: int, value: float):
        """
        Позволяет обновить значение температуры устройства в базе
        :param device_id: id Устройства
        :param value: Значение температуры
        """
        await self.repository.update(
            filter_by_values=dict(id=device_id),
            new_values=dict(temperature=value)
        )
