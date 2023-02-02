"""
Скрипт, который должен запускаться раз в n времени.
В момент запуска ходит в базу, получает сигналы с active == True, затем проверяет значение разности поля
updated_at с datetime.now(). Если разность > поля duration - присваивает значение False для поля active.
"""
import pytest
from datetime import datetime

from repositories import signals_repo, signals_log_repo
from services import device_service


class DataSeeker:
    @classmethod
    async def refresh_rows(cls):
        signals = await signals_repo.do_filter(active=True)
        for signal in signals:
            if not signal.updated_at:
                await signals_repo.update_signal(
                    filter_by_values=dict(id=signal.id),
                    new_values=dict(active=False)
                )
            else:
                date_difference: int = round((signal.updated_at - datetime.now()).total_seconds())
                date_difference *= -1 if date_difference < 0 else date_difference
                if date_difference >= signal.duration:
                    await signals_repo.update_signal(
                        filter_by_values=dict(id=signal.id),
                        new_values=dict(active=False)
                    )
                    if signal.row == "speed_wind":
                        device = await device_service.repository.get(serial=signal.row)
                        await device_service.update_device_wind(device.id, None)
                    elif signal.row == "temper":
                        device = await device_service.repository.get(serial=signal.row)
                        await device_service.update_device_temperature(device.id, None)

                await signals_log_repo.create(signal_id=signal.id, duration=date_difference)
