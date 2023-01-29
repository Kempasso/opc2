from dataclasses import dataclass

from repositories import (
    CodesRepo,
    codes_repo
)


@dataclass
class CodesService:
    repository: CodesRepo = codes_repo

    async def get_codes_by_device_id(self, id: int):
        """
        Позволяет получить все коды для устройства по id устройства
        """
        codes = await self.repository.filter_codes_by_device_id(device_id=id)
        return codes

    async def get_all_codes(self):
        return await self.repository.all()
