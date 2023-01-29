import string
import pytest
import random

from tables import Levels
from repositories import devices_repo, codes_repo, signals_repo, signals_log_repo

CONST_LIMIT = 6


async def create_devices(limit: int = CONST_LIMIT):
    counter = 1
    devices_list: list = []
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
        devices_list.append(device)
        counter += 1
    return devices_list


@pytest.mark.asyncio
async def test_create_devices():
    device_list = await create_devices()
    for el in device_list:
        assert el.id


async def create_codes(device_list: list, limit: int = CONST_LIMIT) -> list:
    codes_list: list = []
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
            code = await codes_repo.create(**data)
            codes_list.append(code)
            counter += 1
    return codes_list


@pytest.mark.asyncio
async def test_create_codes():
    device_list = await create_devices()
    code_list = await create_codes(device_list)
    for el in code_list:
        assert el.id and el.device_id


async def create_signals(device_list: list, code_list: list | None = None, limit: int = CONST_LIMIT):
    signals_list: list = []

    def get_data():
        return dict(
            device_id=device.id,
            duration=random.randint(1, 15),
            active=bool(random.randint(0, 1)),
            # code_id=code.id,
            row="".join(random.choice(string.ascii_letters + string.digits) for i in range(10)),
            description="desc"
        )

    for device in device_list:
        counter = 1
        data = get_data()
        if code_list:
            for code in code_list:
                data["code_id"] = code.id
                signal = signals_repo.create(**data)
                signals_list.append(signal)
        else:
            while counter < limit - 1:
                data = get_data()
                signal = signals_repo.create(**data)
                signals_list.append(signal)

        return signals_list


@pytest.mark.asyncio
async def test_create_signals():
    device_list = await create_devices()
    signals_list = await create_signals(device_list, limit=1)
    for el in signals_list:
        assert el.id and el.device_id


@pytest.mark.asyncio
async def create_signals_log(signals_list: list, limit: int = CONST_LIMIT):
    signals_log_list: list = []
    for signal in signals_list:
        counter = 1
        while counter < limit-1:
            signal_log = await signals_log_repo.create(signal_id=signal.id)
            signals_list.append(signal_log)

    return signals_log_list


@pytest.mark.asyncio
async def test_create_signals_log():
    device_list = await create_devices()
    signals_list = await create_signals(device_list, limit=2)
    signals_log = await create_signals_log(signals_list, limit=2)
    for el in signals_log:
        assert el.id and el.signal_id


async def create_test_data():
    device_list = await create_devices()
    codes_list = await create_codes(device_list, limit=5)
    signals_list = await create_signals(codes_list, limit=5)
    signals_log_list = await create_signals_log(signals_list, limit=2)
