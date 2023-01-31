import re
from datetime import datetime

from services import device_service, signals_service, signals_log_service


class SignalsParser:
    @classmethod
    async def parse_data(cls, data: str, serial: str):

        device = await device_service.repository.get(serial=serial)

        if "temper" in data:
            signal = await signals_service.repository.get(row="temper")
            await signals_service.update(
                filter_by_values=dict(
                    id=signal.id,
                    device_id=device.id
                ),
                new_values=dict(
                    updated_at=datetime.now(),
                    active=True
                )
            )
            temper_value = float(re.findall(r"[-+]?(?:\d*\.*\d+)", data)[0])
            await device_service.update_device_temperature(device.id, temper_value)
            await signals_log_service.repository.create(signal_id=signal.id)
        else:
            elements = data.split(',')
            elements.remove("")
            for el in elements:
                if int(el) < 0:
                    continue
                signal = await signals_service.repository.get(row=el)
                if not signal:
                    continue
                if not signal.active:
                    await signals_service.repository.update(
                        filter_by_values=dict(
                            id=signal.id,
                            device_id=device.id
                        ),
                        new_values=dict(
                            updated_at=datetime.now(),
                            active=True
                        )
                    )
                    await signals_log_service.repository.create(signal_id=signal.id)
                else:
                    await signals_service.repository.update(
                        filter_by_values=dict(
                            id=signal.id,
                            device_id=device.id,
                        ),
                        new_values=dict(
                            updated_at=datetime.now()
                        )
                    )
