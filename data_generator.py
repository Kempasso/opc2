import string
import pytest
import random

from tables import Levels
from repositories import devices_repo, codes_repo, signals_repo, signals_log_repo

CONST_LIMIT = 6


async def create_devices(limit: int = CONST_LIMIT):
    counter = 1
    while counter < limit - 1:
        data = dict(
            title=f"Платформа №{counter}",
            serial=f"Platform0{counter}",
            description=f"Платформа №{counter}",

            model="Платформа СОФ",
            vendor='Филиал УСЗ "Газпром"',
            responsible='Иван Иванов'
        )
        await devices_repo.create(**data)
        counter += 1


@pytest.mark.asyncio
async def test_create_devices():
    device_list = await create_devices()
    for el in device_list:
        assert el.id


async def create_codes(limit: int = CONST_LIMIT):
    device_list = await devices_repo.all(is_query=False)
    for device in device_list:
        counter = 1
        while counter < limit - 1:
            data = dict(
                title=f"Код{counter}",
                level=random.choice([i for i in Levels]),
                description=f"Описание кода №{counter}",
                solution=f"Решение кода №{counter}",
                device_id=device.id
            )
            await codes_repo.create(**data)
            counter += 1


@pytest.mark.asyncio
async def test_create_codes():
    code_list = await create_codes()
    for el in code_list:
        assert el.id and el.device_id


async def create_signals(limit: int = CONST_LIMIT):
    def get_data():
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
    for device in device_list:
        data = get_data()
        if code_list:
            for code in code_list:
                data["code_id"] = code.id
                signal = await signals_repo.create(**data)
                await codes_repo.update(
                    filter_by_values=dict(id=code.id),
                    new_values=dict(signal_id=signal.id)
                )
        else:
            counter = 1
            while counter < limit - 1:
                await signals_repo.create(**get_data())


@pytest.mark.asyncio
async def test_create_signals():
    signals_list = await create_signals(limit=1)
    for el in signals_list:
        assert el.id and el.device_id


@pytest.mark.asyncio
async def create_signals_log(limit: int = CONST_LIMIT):
    signals_list = await signals_repo.all(is_query=False, limit=2)
    for signal in signals_list:
        counter = 1
        while counter < limit-1:
            await signals_log_repo.create(signal_id=signal.id)
            counter += 1


async def create_test_data():
    # await create_devices()
    # await create_codes(limit=5)
    # await create_signals(limit=5)
    await create_signals_log(limit=5)
