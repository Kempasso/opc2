import string
import random
import pytest

from repositories.factories import code_fabric
from repositories import codes_repo, session_maker
from tables import Levels


@pytest.mark.asyncio
async def test_create_code(device):
    device = await device
    data = dict(
        title="".join(random.choice(string.ascii_letters + string.digits) for i in range(10)),
        level=random.choice([i for i in Levels]),
        description="".join(random.choice(string.ascii_letters + string.digits) for i in range(10)),
        solution="".join(random.choice(string.ascii_letters + string.digits) for i in range(10)),
        device_id=device.id
    )
    code = await codes_repo.create(**data)
    assert code.id


@pytest.mark.asyncio
async def test_update_code(code):
    code = await code
    old_values = dict(
        title=code.title,
        description=code.description
    )
    new_values = dict(
        title=code.title[::-1]+" ",
        description=code.description[::-1]+" "
    )
    await codes_repo.update(
        filter_by_values=old_values,
        new_values=new_values
    )
    async with session_maker() as session:
        session.add(code)
        await session.refresh(code)
    assert dict(
        title=code.title,
        description=code.description
    ) != old_values


@pytest.mark.asyncio
async def test_get_by_id_code(code):
    code = await code
    code_instance = await codes_repo.get_by_id(code.id)
    assert code_instance.id


@pytest.mark.asyncio
async def test_do_filter_code(code):
    code = await code
    filtered_values = dict(
        title=code.title,
        description=code.description
    )
    elements = await codes_repo.do_filter(**filtered_values)
    for el in elements:
        assert el
