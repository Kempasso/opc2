import pytest

from services import signals_service, device_service
from signals_parser import SignalsParser


@pytest.mark.asyncio
async def test_parse_data(test_parser_structure):
    test_parser_structure = await test_parser_structure
    data = "17,-18,-19,20,21,-22,23,-24,-25,-26,-44,-46,-27,-28,-29,-30,"
    serial = "STG_01"

    await SignalsParser.parse_data(data, serial)

    codes_list = "17,20,21".split(",")
    device = await device_service.repository.get(serial=serial)
    for code in codes_list:
        signal_instance = await signals_service.repository.get(
            device_id=device.id,
            row=code
        )
        assert signal_instance.active
