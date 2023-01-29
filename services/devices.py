from dataclasses import dataclass

from repositories import (
    DevicesRepo,
    devices_repo
)


@dataclass
class DeviceService:
    repository: DevicesRepo = devices_repo

    async def get_all_devices(self):
        """
        Позволяет получить все устройства
        """
        devices = await self.repository.all()
        return devices

    async def get_device_by_id(self, id: int):
        """
        Позволяет получить устройство по его id=
        """
        device = await self.repository.get_by_id(id)
        return device
