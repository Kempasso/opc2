from typing import Any

from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.async_sqlalchemy import paginate

from services import signals_service
from . import get_session, AsyncSession, response_models as rm


router = APIRouter()


@router.post(path="/load")
async def load(data: str):
    signals_service.parse_signal(data)


@router.get(path="/{id}", response_model=rm.SignalResponseModel)
async def get_signal_by_code_id(id: int) -> rm.SignalResponseModel:
    """
    Позволяет получить сигнал по id кода
    """
    signal = await signals_service.get_signal_by_code_id(id=id)
    return rm.SignalResponseModel(**vars(signal))


@router.get(path="/device/{id}/active", response_model=Page[rm.SignalResponseModel])
async def get_active_signals_by_device(id: int,
                                       session: AsyncSession = Depends(get_session),
                                       params: Params = Depends()
                                       ) -> AbstractPage[rm.SignalsLogsResponseModel]:
    signals_query = await signals_service.get_active_signals_by_device_id(id=id)
    return await paginate(conn=session, query=signals_query, params=params)


@router.get(path="", response_model=Page[rm.SignalResponseModel])
async def get_all_signals(session: AsyncSession = Depends(get_session),
                          params: Params = Depends()
                          ) -> AbstractPage[rm.SignalsResponseModel]:
    """
    Позволяет получить все устройства
    """
    query = await signals_service.get_all_signals()
    return await paginate(conn=session, query=query, params=params)
