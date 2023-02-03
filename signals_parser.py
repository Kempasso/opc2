import re
from datetime import datetime

from services import device_service, signals_service, signals_log_service
from tables import SignalLevels


class SignalsParser:
    @classmethod
    async def parse_data(cls, row: str, serial: str):

        device = await device_service.repository.get(serial=serial)

        if "temper" in row:
            signal = await signals_service.repository.get(row="temper", device_id=device.id)
            temper_value = float(re.findall(r"[-+]?(?:\d*\.*\d+)", row)[0])
            temper_level: SignalLevels = SignalLevels.info
            if temper_value in range(-35, -25) or temper_value in range(25, 35):
                temper_level = SignalLevels.warning
            elif temper_value < 35 or temper_value > 35:
                temper_level = SignalLevels.error
            await signals_service.update(
                filter_by_values=dict(
                    id=signal.id,
                    device_id=device.id
                ),
                new_values=dict(
                    updated_at=datetime.now(),
                    active=True,
                    level=temper_level
                )
            )
            await device_service.update_device_temperature(device.id, temper_value)
            await signals_log_service.repository.create(signal_id=signal.id)

        elif "speed_wind" in row:
            signal = await signals_service.repository.get(row="speed_wind", device_id=device.id)
            wind_value = float(re.findall(r"[-+]?(?:\d*\.*\d+)", row)[0])
            wind_level: SignalLevels = SignalLevels.info
            if round(wind_value) in range(15, 30):
                wind_level = SignalLevels.warning
            elif round(wind_value) > 30:
                wind_level = SignalLevels.error
            await signals_service.repository.update(
                filter_by_values=dict(
                    id=signal.id,
                    device_id=device.id,
                ),
                new_values=dict(
                    updated_at=datetime.now(),
                    active=True,
                    level=wind_level
                )
            )
            await device_service.update_device_wind(device.id, wind_value)
            await signals_log_service.repository.create(signal_id=signal.id)
        else:
            elements = row.split(',')
            elements.remove("")
            for el in elements:
                if int(el) < 0:
                    continue
                signal = await signals_service.repository.get(row=el, device_id=device.id)
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
