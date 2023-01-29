from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.async_sqlalchemy import paginate

from services import codes_service
from . import get_session, AsyncSession, response_models as rm

router = APIRouter()


@router.get(path="/{id}", response_model=Page[rm.CodeResponseModel])
async def get_codes_by_device_id(id: int,
                                 session: AsyncSession = Depends(get_session),
                                 params: Params = Depends()
                                 ) -> rm.CodesResponseModel:
    codes_query = await codes_service.get_codes_by_device_id(id=id)
    return await paginate(conn=session, query=codes_query, params=params)


@router.get(path="", response_model=Page[rm.CodeResponseModel])
async def get_all_codes(session: AsyncSession = Depends(get_session),
                        params: Params = Depends()
                        ) -> rm.CodesResponseModel:
    codes_query = await codes_service.get_all_codes()
    return await paginate(conn=session, query=codes_query, params=params)
