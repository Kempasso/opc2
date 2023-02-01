import pytest

from data_seeker import DataSeeker


@pytest.mark.asyncio
async def test_refresh_rows():
    await DataSeeker.refresh_rows()
