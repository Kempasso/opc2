from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.async_sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from api import response_models as rm, get_session
from services import signals_log_service

router = APIRouter()


@router.get(path="", response_model=Page[rm.SignalsLogResponseModel])
async def get_all_log_entries(
        session: AsyncSession = Depends(get_session),
        params: Params = Depends()
) -> AbstractPage[rm.SignalsLogResponseModel]:
    """
    Позволяет получить все записи лога сигналов
    """
    logs_query = await signals_log_service.get_all_log_entries()
    return await paginate(conn=session, query=logs_query, params=params)


@router.get(path="/log/device/{id}", response_model=Page[rm.SignalsLogResponseModel])
async def get_log_entries_by_device_id(
        id: int,
        session: AsyncSession = Depends(get_session),
        params: Params = Depends()
) -> AbstractPage[rm.SignalsLogResponseModel]:
    """
    Позволяет получить записи лога сигналов по id устройства
    """
    logs_query = await signals_log_service.filter_log_entries_by_device_id(id)
    return await paginate(conn=session, query=logs_query, params=params)
