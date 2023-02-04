import random
import string
import pytest

from repositories import (
    signals_repo,
    session_maker
)
from tables import SignalLevels


# SignalsRepo tests
@pytest.mark.asyncio
async def test_create_signal(device, code):
    device = await device
    code = await code
    data = dict(
        device_id=device.id,
        duration=random.randint(1, 15),
        active=bool(random.randint(0, 1)),
        level=random.choice([i for i in SignalLevels]),
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
