import random
import pytest

from repositories.factories import (
    device_fabric,
    code_fabric,
    signal_fabric,
    signal_log_fabric,
)
from repositories import (
    signals_repo,
    signals_log_repo,
    codes_repo,
)
from tables import Levels


@pytest.fixture
async def device():
    new_instance = await device_fabric.generate()
    return new_instance


@pytest.fixture
async def code():
    device_instance = await device_fabric.generate()
    code_number = random.randint(1, 100)
    data = dict(
        title=f"Код {code_number}",
        level=random.choice([i for i in Levels]),
        description=f"Описание кода №{code_number}",
        solution=f"Решение кода №{code_number}",
        device_id=device_instance.id
    )
    new_instance = await codes_repo.create(**data)
    return new_instance


@pytest.fixture
async def signal():
    device = await device_fabric.generate()
    data = dict(
        device=device,
        duration=5,
        row="-12,41,53",
        description="Без описания",
    )
    new_instance = await signals_repo.create(**data)
    return new_instance


@pytest.fixture
async def signal_log():
    device = await device_fabric.generate()
    data = dict(
        device=device,
        duration=5,
        row="-12,41,53",
        description="Без описания",
    )
    new_signal_instance = await signals_repo.create(**data)
    data = dict(
        signal=new_signal_instance
    )
    new_instance = await signals_log_repo.create(**data)
    return new_instance
