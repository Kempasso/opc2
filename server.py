import sys
import uvicorn
from fastapi import FastAPI

import settings
from api import DeviceRouter, SignalRouter, CodesRouter, SignalLogsRouter
from repositories import create_tables
from data_generator import create_test_data

from fastapi_pagination import add_pagination


application = FastAPI()


@application.on_event("startup")
async def init_tables():
    await create_tables()


application.include_router(DeviceRouter, prefix="/api/devices")
application.include_router(SignalRouter, prefix="/api/signals")
application.include_router(CodesRouter, prefix="/api/codes")
application.include_router(SignalLogsRouter, prefix="/api/signal_logs")

add_pagination(application)

HELP_MESSAGE = """
Available commands:
1. runserver
2. create_test_data
"""

if __name__ == "__main__":
    if "runserver" in sys.argv:
        uvicorn.run(app=application, host=settings.HOST, port=settings.PORT)
    elif "create_test_data" in sys.argv:
        settings.EVENT_LOOP.run_until_complete(init_tables())
        settings.EVENT_LOOP.run_until_complete(create_test_data())
    else:
        print(HELP_MESSAGE)
