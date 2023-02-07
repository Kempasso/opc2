import argparse
import json

from repositories import (
    devices_repo,
    signals_repo,
    create_tables
)
from tables import SignalLevels
from settings import EVENT_LOOP
from enum import Enum


DESCRIPTION = """
Программа, реализующая механизм генерации экземпляров данных
устройств и сигналов для них.
"""

argument_parser = argparse.ArgumentParser(
    prog="data_comparator.py",
    description=DESCRIPTION,
    epilog="Коды для устройств находятся в папке codes")
argument_parser.add_argument('run', help="Запускает генерацию устройств.", type=bool)


class DeviceAmounts(Enum):
    platform = 8
    gate = 10
    crane = 1


class Devices(Enum):
    """
    amount -- количество устройств для генерации
    file -- .json файл с кодами
    """
    platform = dict(
        model='Платформа СОФ',
        title='Платформа №',
        serial='Platform',
        description=None,
        amount=DeviceAmounts.platform.value,
        file="codes_platform.json",
        responsible='Господин Филиал УСЗ ПАО "Газпром"',
        vendor='Филиал УСЗ ПАО "Газпром"'
    )
    gate = dict(
        model='Система Технических Ворот',
        title='Ворота №',
        serial='STG',
        description='СТВ',
        amount=DeviceAmounts.gate.value,
        file="codes_gate.json",
        responsible='Иван Иванов',
        vendor='Филиал УСЗ ПАО "Газпром"'
    )
    crane = dict(
        model='Кран СОФ',
        title='Кран ',
        serial='crane',
        description=None,
        amount=DeviceAmounts.crane.value,
        file="codes_crane.json",
        responsible='Иван Иванов',
        vendor='Филиал УСЗ ПАО "Газпром"'
    )


class DataComparator:
    _levels = {"20": SignalLevels.info, "30": SignalLevels.warning, "40": SignalLevels.error}

    @classmethod
    async def parse_codes_from_json(cls, file: str) -> list:
        with open(f"codes/{file}") as opened_file:
            return json.load(opened_file)['data']

    @classmethod
    async def create_codes_from_file_for_device(cls, device_id: int, file: str):
        codes = await cls.parse_codes_from_json(file=file)
        for code in codes:
            await signals_repo.create(
                row=code['code'],
                device_id=device_id,
                level=cls._levels[str(code['level'])],
                description=code['description'],
            )

    @classmethod
    async def create_base_devices(cls):
        async def get_data(device: Devices) -> list[dict]:
            data: list = []
            counter = 0
            while counter < device['amount']:
                data.append(dict(
                    title=device['title'] + str(counter + 1),
                    serial=device['serial'] + f"0{counter+1}" if counter + 1 < 10 else device['serial'] + f"{counter + 1}",
                    description=device['description'] if device['description'] else device['model'],
                    model=device['model'],
                    responsible='Иван Иванов',
                    vendor='Филиал УСЗ Газпром'
                    )
                )
                counter += 1
            return data

        for device in Devices:
            device = device.value
            data = await get_data(device)
            for data_unit in data:
                device_instance = await devices_repo.create(**data_unit)
                await cls.create_codes_from_file_for_device(
                    device_id=device_instance.id,
                    file=device['file']
                )


if 'run' in vars(argument_parser.parse_args()):
    EVENT_LOOP.run_until_complete(create_tables())
    EVENT_LOOP.run_until_complete(DataComparator.create_base_devices())
