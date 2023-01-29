import random
import string
import pytest

from repositories.factories import signal_fabric, signal_log_fabric
from repositories import (
    signals_repo,
    signals_log_repo,
    session_maker
)


# SignalsRepo tests
@pytest.mark.asyncio
async def test_create_signal(device, code):
    device = await device
    code = await code
    data = dict(
        device_id=device.id,
        duration=random.randint(1, 15),
        active=bool(random.randint(0, 1)),
        code_id=code.id,
        row="".join(random.choice(string.ascii_letters + string.digits) for i in range(10)),
        description="desc"
    )
    signal = await signals_repo.create(**data)
    assert signal.id


@pytest.mark.asyncio
async def test_update_signal(signal):
    signal = await signal
    old_values = dict(
        row=signal.row,
        duration=signal.duration
    )
    new_values = dict(
        row=signal.row,
        duration=signal.duration**2
    )
    await signals_repo.update(
        filter_by_values=old_values,
        new_values=new_values
    )
    async with session_maker() as session:
        session.add(signal)
        await session.refresh(signal)
    assert dict(
        row=signal.row,
        duration=signal.duration
    ) != old_values


@pytest.mark.asyncio
async def test_get_by_id_signal(signal):
    signal = await signal
    signal_instance = await signals_repo.get_by_id(signal.id)
    assert signal.id


@pytest.mark.asyncio
async def test_do_filter_signal(signal):
    signal = await signal
    filtered_values = dict(
        row=signal.row,
        duration=signal.duration,
    )
    elements = await signals_repo.do_filter(**filtered_values)
    for el in elements:
        assert el


# SignalsLogRepo tests
@pytest.mark.asyncio
async def test_create_signals_log(signal):
    signal = await signal
    data = dict(
        signal_id=signal.id
    )
    signals_log = await signals_log_repo.create(**data)
    assert signals_log.id


@pytest.mark.asyncio
async def test_get_by_id_signals_log(signal_log):
    signal_log = await signal_log
    signal_instance = await signals_log_repo.get_by_id(signal_log.id)
    assert signal_instance.id


@pytest.mark.asyncio
async def test_do_filter_signals_log(signal_log):
    signal_log = await signal_log
    filtered_values = {
        # signal.device_id: signal_log.signal.device_id,
    }
    elements = await signals_log_repo.do_filter(**filtered_values)
    for el in elements:
        assert el


@pytest.mark.asyncio
async def test_filter_signals_by_device_id(signal_log):
    signal_log = await signal_log
    elements = await signals_log_repo.filter_signals_by_device_id(signal_log.signal.device_id)
    for el in elements:
        assert el
