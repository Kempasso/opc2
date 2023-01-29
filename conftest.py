import pathlib
import sys

import pytest

app_path = pathlib.Path.cwd()
sys.path.append(app_path.as_posix())

from repositories import create_tables
from settings import EVENT_LOOP


@pytest.fixture(scope="session")
def event_loop():
    return EVENT_LOOP


def pytest_sessionstart(session):
    """
    Инициализация слоёв таблиц и репозиториев
    """
    EVENT_LOOP.run_until_complete(create_tables())


def pytest_sessionfinish(session, exitstatus):
    EVENT_LOOP.close()
