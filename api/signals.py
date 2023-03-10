from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.async_sqlalchemy import paginate

from pydantic import BaseModel

from services import signals_service
from signals_parser import SignalsParser
from . import get_session, AsyncSession, response_models as rm


router = APIRouter()


class OPCDataSchema(BaseModel):
    row: str
    serial: str


@router.post(path="/load", status_code=201)
async def load(data: OPCDataSchema):
    """
    Эндпоинт для обработки данных с OPC-клиента
    """
    await SignalsParser.parse_data(data.row, data.serial)
    return {"message": "Created"}


@router.get(path="/{id}", response_model=rm.SignalResponseModel)
async def get_signal_by_code_id(id: int) -> rm.SignalResponseModel:
    """
    Позволяет получить сигнал по id его кода
    """
    signal = await signals_service.get_signal_by_code_id(id=id)
    return rm.SignalResponseModel(**vars(signal))


@router.get(path="/device/{id}", response_model=Page[rm.SignalResponseModel])
async def get_signals_by_device_id(id: int,
                               session: AsyncSession = Depends(get_session),
                               params: Params = Depends()) -> AbstractPage[rm.SignalsResponseModel]:
    """
    Позволяет получить все сигналы по id устройства
    """
    signals_query = await signals_service.get_signals_by_device_id(id=id)
    return await paginate(conn=session, query=signals_query, params=params)


@router.get(path="/device/{id}/active", response_model=Page[rm.SignalResponseModel])
async def get_active_signals_by_device_id(id: int,
                                       session: AsyncSession = Depends(get_session),
                                       params: Params = Depends()
                                       ) -> AbstractPage[rm.SignalsResponseModel]:
    """
    Позволяет получить активные сигналы устройства
    """
    signals_query = await signals_service.get_active_signals_by_device_id(id=id)
    return await paginate(conn=session, query=signals_query, params=params)


@router.get(path="", response_model=Page[rm.SignalResponseModel])
async def get_all_signals(session: AsyncSession = Depends(get_session),
                          params: Params = Depends()
                          ) -> AbstractPage[rm.SignalsResponseModel]:
    """
    Позволяет получить все сигналы
    """
    query = await signals_service.get_all_signals()
    return await paginate(conn=session, query=query, params=params)
