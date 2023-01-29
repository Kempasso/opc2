import typing
from datetime import datetime

from tables import Device
from tables.codes import Levels

from pydantic import BaseModel


class DeviceResponseModel(BaseModel):
    id: int
    title: str
    serial: str
    description: str
    responsible: str
    model: str
    vendor: str

    created_at: datetime | None
    updated_at: datetime | None

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True


class DevicesResponseModel(BaseModel):
    __root__ = typing.List[DeviceResponseModel]

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True


class SignalResponseModel(BaseModel):
    id: int
    device_id: int | None
    code_id: int | None
    active: bool
    description: str

    created_at: datetime | None
    updated_at: datetime | None

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True


class SignalsResponseModel(BaseModel):
    __root__ = typing.List[SignalResponseModel]

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True


class SignalsLogResponseModel(BaseModel):
    id: int
    signal_id: int

    created_at: datetime
    updated_at: datetime | None

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True


class SignalsLogsResponseModel(BaseModel):
    __root__ = typing.List[SignalsLogResponseModel]

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True


class CodeResponseModel(BaseModel):
    id: int
    title: str
    level: Levels
    description: str
    solution: str

    device_id: int | None

    signal_id: int | None

    created_at: datetime | None
    updated_at: datetime | None

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True


class CodesResponseModel(BaseModel):
    __root__ = typing.List[CodeResponseModel]

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True
