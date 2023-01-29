import pytest


@pytest.mark.asyncio
async def test_get_device_by_id(test_client, device):
    device = await device
    response = test_client.get(f"/api/devices/{device.id}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_all_devices(test_client):
    # device = await device
    response = test_client.get(f"/api/devices")
    assert response.status_code == 200
