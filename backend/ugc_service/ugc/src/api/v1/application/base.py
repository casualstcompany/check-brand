from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core import deps
from crud.application import application_crud
from schemas.error import DetailResponse
from services.application import application_service

base_error_response = {
    400: {"model": DetailResponse},
    401: {"model": DetailResponse},
    403: {"model": DetailResponse},
    404: {"model": DetailResponse}
}


class BaseApplicationAPI:
    db: AsyncSession = Depends(deps.get_async_db)
    service = application_service
    crud = application_crud
