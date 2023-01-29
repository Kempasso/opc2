from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.async_sqlalchemy import paginate


from services import device_service
from . import get_session, AsyncSession, response_models as rm


router = APIRouter()


@router.get(path="/{id}", response_model=rm.DeviceResponseModel)
async def get_device_by_id(id: int) -> rm.DeviceResponseModel:
    """
    Позволяет получить устройство по его id
    """
    device = await device_service.get_device_by_id(id=id)
    return rm.DeviceResponseModel(**vars(device))


@router.get(path="", response_model=Page[rm.DeviceResponseModel])
async def get_all_devices(session: AsyncSession = Depends(get_session),
                          params: Params = Depends()) -> rm.DevicesResponseModel:
    """
    Позволяет получить все устройства
    """
    devices_query = await device_service.get_all_devices()
    return await paginate(conn=session, query=devices_query, params=params)
    # return rm.DevicesResponseModel(**vars(devices))
