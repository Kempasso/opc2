import pytest


@pytest.mark.asyncio
async def test_get_codes_by_device_id(test_client, device):
    device = await device

    response = test_client.get(f"/api/codes/{device.id}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_codes_by_device_id_filtered_by_active_signals(test_client, code, device):
    code = await code
    device = await device

    response = test_client.get(f"/api/codes/{device.id}/active")
    assert response.status_code == 200
