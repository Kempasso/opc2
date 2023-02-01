import random
import pytest

from tables import SignalLevels
from repositories import devices_repo, signals_repo


@pytest.fixture
async def test_parser_structure():
    data = dict(
        title="Ворота №1",
        serial="STG_01",
        description="Ворот",
        model="Технические ворота СОФ",
        vendor="Vendor",
        responsible="Ответственный",
    )
    device_instance = await devices_repo.create(**data)
    codes_list = "17,20,21"
    for code in codes_list.split(","):
        data = dict(
            row=code,
            level=random.choice([i for i in SignalLevels]),
            description=f"Описание кода №{code}",
            solution=f"Решение кода №{code}",
            device_id=device_instance.id
        )
        await signals_repo.create(**data)
