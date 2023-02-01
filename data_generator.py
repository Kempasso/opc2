"""
Генератор тестовых данных.
"""

import string
import pytest
import random

from tables import Levels
from repositories import devices_repo, codes_repo, signals_repo, signals_log_repo


class DataGenerator:
    CONST_LIMIT: int = 6

    @classmethod
    async def create_devices(cls, limit: int = CONST_LIMIT) -> list[int]:
        counter = 0
        device_ids: list = []
        while counter < limit - 1:
            data = dict(
                title=f"Платформа №{counter}",
                serial=f"Platform0{counter}",
                description=f"Платформа №{counter}",

                model="Платформа СОФ",
                vendor='Филиал УСЗ "Газпром"',
                responsible='Иван Иванов'
            )
            device = await devices_repo.create(**data)
            device_ids.append(device.id)
            counter += 1
        return device_ids

    @classmethod
    async def create_codes(cls, limit: int = CONST_LIMIT) -> list[int]:
        device_list = await devices_repo.all(is_query=False)
        codes_ids: list = []
        for device in device_list:
            counter = 0
            while counter < limit - 1:
                data = dict(
                    title=f"Код{counter+1}",
                    level=random.choice([i for i in Levels]),
                    description=f"Описание кода №{counter+1}",
                    solution=f"Решение кода №{counter+1}",
                    device_id=device.id
                )
                code = await codes_repo.create(**data)
                codes_ids.append(code.id)
                counter += 1
        return codes_ids

    @classmethod
    async def create_signals(cls, limit: int = CONST_LIMIT) -> list[int]:
        async def get_data() -> dict:
            return dict(
                device_id=device.id,
                duration=random.randint(1, 15),
                active=True,
                # code_id=code.id,
                row="".join(random.choice(string.ascii_letters + string.digits) for i in range(10)),
                description="desc"
            )

        device_list = await devices_repo.all(is_query=False)
        code_list = await codes_repo.all(is_query=False, limit=2)
        signals_ids: list = []
        for device in device_list:
            data = await get_data()
            if code_list:
                for code in code_list:
                    data["code_id"] = code.id
                    signal = await signals_repo.create(**data)
                    signals_ids.append(signal.id)
                    await codes_repo.update(
                        filter_by_values=dict(id=code.id),
                        new_values=dict(signal_id=signal.id)
                    )
            else:
                counter = 0
                while counter < limit:
                    signal = await signals_repo.create(**await get_data())
                    signals_ids.append(signal.id)
        return signals_ids

    @classmethod
    async def create_signals_log(cls, limit: int = CONST_LIMIT) -> list[int]:
        signals_list = await signals_repo.all(is_query=False, limit=2)
        signals_log_ids: list = []
        for signal in signals_list:
            counter = 0
            while counter < limit-1:
                signal_log = await signals_log_repo.create(signal_id=signal.id)
                signals_log_ids.append(signal_log.id)
                counter += 1
        return signals_log_ids

    @classmethod
    async def create_test_data(cls, limit: int = CONST_LIMIT):
        await cls.create_devices(limit)
        await cls.create_codes(limit)
        await cls.create_signals(limit)
        await cls.create_signals_log(limit)
