import pytest


@pytest.mark.asyncio
async def test_get_signal_by_code_id(test_client, code_api):
    code_api = await code_api
    response = test_client.get(f"/api/signals/{code_api.id}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_active_signals_by_device_id(test_client, test_signal_structure):
    device = await test_signal_structure
    response = test_client.get(f"/api/signals/device/{device.id}/active")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_all_signals(test_client):
    response = test_client.get("/api/signals")
    assert response.status_code == 200
