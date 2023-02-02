import sys
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


import settings
from api import DeviceRouter, SignalRouter, CodesRouter, SignalLogsRouter
from repositories import create_tables

from fastapi_pagination import add_pagination


application = FastAPI()


@application.on_event("startup")
async def init_tables():
    await create_tables()

application.include_router(DeviceRouter, prefix="/api/devices")
application.include_router(SignalRouter, prefix="/api/signals")
application.include_router(CodesRouter, prefix="/api/codes")
application.include_router(SignalLogsRouter, prefix="/api/signal_logs")

application.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

add_pagination(application)

if __name__ == "__main__":
    uvicorn.run(app=application, host=settings.HOST, port=settings.PORT)
    settings.EVENT_LOOP.run_until_complete(init_tables())
