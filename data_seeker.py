"""
Скрипт, который должен запускаться раз в n времени.
В момент запуска ходит в базу, получает сигналы с active == True, затем проверяет значение разности поля
updated_at с datetime.now(). Если разность > поля duration - присваивает значение False для поля active.
"""
import pytest
from datetime import datetime

from repositories import signals_repo, signals_log_repo


async def refresh_rows():
    signals = await signals_repo.do_filter(active=True)
    for signal in signals:
        if not signal.updated_at or signal.updated_at - datetime.now() >= signal.duration:
            await signals_repo.update(
                filter_by_values=dict(id=signal.id),
                new_values=dict(active=False)
            )
            await signals_log_repo.create(signal_id=signal.id)
