import pytest

from services import device_service
from repositories import session_maker


@pytest.mark.asyncio
async def test_update_device_temperature(device):
    device = await device
    temp_value = 32.2
    await device_service.update_device_temperature(device.id, temp_value)
    async with session_maker() as session:
        session.add(device)
        await session.refresh(device)
    assert device.temperature == temp_value


@pytest.mark.asyncio
async def test_update_device_wind(device):
    device = await device
    wind_value = 12.2
    await device_service.update_device_wind(device.id, wind_value)
    async with session_maker() as session:
        session.add(device)
        await session.refresh(device)
    assert device.wind == wind_value
