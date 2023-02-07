import asyncio

import pathlib
import logging
import sys


class Logger:
    def __init__(self):
        self._logger = logging.getLogger()
        self._logger.setLevel(logging.DEBUG)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)

    def info(self, msg: str):
        self._logger.info(msg=msg)

    def debug(self, msg: str):
        self._logger.debug(msg=msg)

    def warning(self, msg: str):
        self._logger.warning(msg=msg)


LOGGER = Logger()
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

EVENT_LOOP_POLICY = asyncio.get_event_loop_policy()
EVENT_LOOP = asyncio.new_event_loop()
EVENT_LOOP_POLICY.set_event_loop(EVENT_LOOP)

HOST = "127.0.0.1"
PORT = 8080
DB_URL = "postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/FastAPI"

CORS_ORIGINS = [
    "http://172.19.19.26:8069/"
]
