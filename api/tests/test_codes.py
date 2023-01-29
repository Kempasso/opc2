import pytest


@pytest.mark.asyncio
async def test_get_codes_by_device_id(test_client, device, code):
    code = await code
    device = await device
    response = test_client.get(f"/api/codes/{device.id}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_all_codes(test_client, code):
    code = await code
    response = test_client.get("/api/codes")
    assert response.status_code == 200
