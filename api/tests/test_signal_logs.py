import pytest


@pytest.mark.asyncio
async def test_get_all_log_entries(test_client):
    response = test_client.get("/api/signal_logs")
    assert response.status_code == 200
