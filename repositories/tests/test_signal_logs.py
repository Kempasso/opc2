import pytest

from repositories import signals_log_repo


@pytest.mark.asyncio
async def test_create_signals_log(signal):
    signal = await signal
    data = dict(
        signal_id=signal.id
    )
    signals_log = await signals_log_repo.create(**data)
    assert signals_log.id


# @pytest.mark.asyncio
# async def test_get_by_id_signals_log(signal_log):
#     signal_log = await signal_log
#     signal_instance = await signals_log_repo.get_by_id(signal_log.id)
#     assert signal_instance.id
#
#
# @pytest.mark.asyncio
# async def test_do_filter_signals_log(signal_log):
#     signal_log = await signal_log
#     filtered_values = {
#         # signal.device_id: signal_log.signal.device_id,
#     }
#     elements = await signals_log_repo.do_filter(**filtered_values)
#     for el in elements:
#         assert el
#
#
# @pytest.mark.asyncio
# async def test_filter_signals_by_device_id(signal_log):
#     signal_log = await signal_log
#     elements = await signals_log_repo.filter_signals_by_device_id(signal_log.signal.device_id)
#     for el in elements:
#         assert el
