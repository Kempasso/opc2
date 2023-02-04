import random
import string

import pytest
from fastapi.testclient import TestClient

from repositories import (
    factories,
    signals_repo,
    codes_repo,
    devices_repo
)
from tables import CodeLevels, SignalLevels
from server import application


@pytest.fixture
def test_client(event_loop):
    with TestClient(app=application) as client:
        yield client


@pytest.fixture
async def device():
    new_instance = await devices_repo.create(
        title="Платформа №1",
        serial="STG_01",
        description="Description",
        model="Платформа СОФ",
        responsible='Иван Иванов',
        vendor='Филиал УСЗ Газпром'
    )
    return new_instance


@pytest.fixture
async def signal(device):
    device = await device
    new_instance = await signals_repo.create(
            device_id=device.id,
            duration=random.randint(5, 15),
            level=random.choice([i for i in SignalLevels]),
            active=bool(random.randint(0, 1)),
            row="17",
            description="".join(random.choice(string.ascii_letters + string.digits) for i in range(10)),
    )
    return new_instance


@pytest.fixture
async def code():
    device_instance = await factories.device_fabric.generate()
    code_number = random.randint(1, 100)
    data = dict(
        title=f"Код {code_number}",
        level=random.choice([i for i in CodeLevels]),
        description=f"Описание кода №{code_number}",
        solution=f"Решение кода №{code_number}",
        device_id=device_instance.id
    )
    new_instance = await codes_repo.create(**data)

    return new_instance


@pytest.fixture
async def test_signal_structure():
    device = await factories.device_fabric.generate()
    code_number = random.randint(1, 100)
    data = dict(
        title=f"Код {code_number}",
        level=random.choice([i for i in CodeLevels]),
        description=f"Описание кода №{code_number}",
        solution=f"Решение кода №{code_number}",
        device_id=device.id
    )
    code = await codes_repo.create(**data)
    data = dict(
        device_id=device.id,
        duration=random.randint(5, 15),
        level=random.choice([i for i in SignalLevels]),
        active=bool(random.randint(0, 1)),
        code_id=code.id,
        row="".join(random.choice(string.ascii_letters + string.digits) for i in range(10)),
        description="".join(random.choice(string.ascii_letters + string.digits) for i in range(10)),
    )
    signal = await signals_repo.create(**data)
    return device


@pytest.fixture
async def code_api():
    device = await factories.device_fabric.generate()
    code_number = random.randint(1, 100)
    data = dict(
        title=f"Код {code_number}",
        level=random.choice([i for i in CodeLevels]),
        description=f"Описание кода №{code_number}",
        solution=f"Решение кода №{code_number}",
        device_id=device.id
    )
    code = await codes_repo.create(**data)
    new_signal = await signals_repo.create(
        device_id=device.id,
        duration=5,
        active=True,
        level=random.choice([i for i in SignalLevels]),
        code_id=code.id,
        row="TEST",
        description="Description"
    )

    return code
