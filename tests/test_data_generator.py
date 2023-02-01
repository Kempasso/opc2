import pytest

from data_generator import DataGenerator


@pytest.mark.asyncio
async def test_create_devices():
    device_list = await DataGenerator.create_devices()
    assert device_list


@pytest.mark.asyncio
async def test_create_codes():
    code_list = await DataGenerator.create_codes(limit=2)
    assert code_list


@pytest.mark.asyncio
async def test_create_signals():
    signals_list = await DataGenerator.create_signals(limit=2)
    assert signals_list


@pytest.mark.asyncio
async def test_create_signals_log():
    signals_log = await DataGenerator.create_signals_log(limit=2)
    assert signals_log
