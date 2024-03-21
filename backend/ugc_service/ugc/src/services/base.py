from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession

from core.utils import validate_uuid4
from crud.base import crud_base


class BaseService(ABC):
    crud = crud_base

    def __int__(self):
        pass

    async def get(self, db: AsyncSession, obj_id: str):
        if not await validate_uuid4(obj_id):
            return None
        application = await self.crud.get(db, id=obj_id)
        return application
