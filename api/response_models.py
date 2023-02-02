import typing
from datetime import datetime

from tables import Device
from tables import SignalLevels, CodeLevels

from pydantic import BaseModel


class DeviceResponseModel(BaseModel):
    id: int
    title: str
    serial: str
    description: str

    temperature: float | None
    wind: float | None

    created_at: datetime | None
    updated_at: datetime | None

    responsible: str
    model: str | None
    vendor: str

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

    duration: int | None
    active: bool
    level: SignalLevels
    description: str | None
    solution: str | None
    row: str

    code_id: int | None

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
    duration: int | None

    signal: SignalResponseModel

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
    level: CodeLevels
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
