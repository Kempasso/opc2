import pytest

from repositories.factories import device_fabric
from repositories import devices_repo, session_maker


@pytest.mark.asyncio
async def test_create_device():
    device = await device_fabric.generate()
    assert device.id


@pytest.mark.asyncio
async def test_update_device(device):
    device = await device
    old_values = dict(
        title=device.title,
        serial=device.serial
    )
    new_values = dict(
        title=device.title[::-1]+"--",
        serial=device.serial[::-1]+"--",
    )
    await devices_repo.update(
        filter_by_values=old_values,
        new_values=new_values
    )
    async with session_maker() as session:
        session.add(device)
        await session.refresh(device)
    assert dict(
        title=device.title,
        serial=device.serial
    ) != old_values


@pytest.mark.asyncio
async def test_get_by_id_device(device):
    device = await device
    device_instance = await devices_repo.get_by_id(device.id)
    assert device_instance.id


@pytest.mark.asyncio
async def test_do_filter_device(device):
    device = await device
    filtered_values = dict(
        title=device.title,
        description=device.description
    )
    elements = await devices_repo.do_filter(**filtered_values)
    for el in elements:
        assert el
