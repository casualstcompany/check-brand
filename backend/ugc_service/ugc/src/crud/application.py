from typing import Any, Optional

from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.sql.expression import and_
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase, ModelType
from models.application import Application
from schemas.base import BaseSchema
from schemas.application import (UserCreateApplicationInnerSchema, UserEditApplicationInnerSchema)


class CRUDApplication(CRUDBase[Application, UserCreateApplicationInnerSchema, UserEditApplicationInnerSchema]):

    async def get_by_list_token(self, db: AsyncSession, data: BaseSchema):
        objs = await db.scalars(select(self.model).filter(
            self.model.token_id.in_(data.tokens),
            self.model.hide == False
        ))
        return objs.all()

    async def get_object_list_query(self, params: dict, sort: Optional[str] = None):
        """Формирует запрос к БД"""
        order_by = await self.get_order_by(sort)
        new_select = select(self.model)

        new_select = new_select.where(self.model.hide == False)
        search = params.get("search")
        if search and search.get('q') and search.get('search_fields'):
            new_select = new_select.where(
                # TODO: Проверить на SQL инъекции
                or_(getattr(self.model, key).ilike(f'%{search.get("q")}%') for key in search.get('search_fields'))
            )

        range_gt = params.get("range_gt")
        if range_gt:
            for key in range_gt:
                new_select = new_select.where(and_(getattr(self.model, key) > range_gt.get(key)))

        params_in = params.get("in_values")
        if params_in:
            for key in params_in:
                new_select = new_select.where(and_(getattr(self.model, key).in_(params_in.get(key))))

        params.pop("search")
        params.pop("in_values")
        params.pop("range_gt")
        new_select = new_select.filter_by(**params).order_by(order_by)

        return new_select

    async def get_by_collection_and_token_not_null(self, db: AsyncSession, collection_id: str) -> Optional[ModelType]:
        objs = await db.scalars(select(self.model).filter(
            self.model.collection_id == collection_id,
            self.model.token_id.isnot(None),
            self.model.hide == False
        ))
        return objs.all()

    async def get_order_by(self, sort: Optional[str] = None):
        if sort == "-updated_at":
            order_by = self.model.updated_at.desc()
        elif sort == "updated_at":
            order_by = self.model.updated_at.asc()
        elif sort == "-created_at":
            order_by = self.model.created_at.desc()
        else:
            order_by = self.model.created_at.asc()
        return order_by

    async def get_by_wallet_and_token_not_null_query(self, wallet: str, sort: Optional[str] = None):

        order_by = await self.get_order_by(sort)
        query = select(self.model).filter(
            self.model.user_wallet == wallet,
            self.model.token_id.isnot(None),
            self.model.hide == False
        ).order_by(order_by)

        return query

    async def get_count_status_by_collection(self, db: AsyncSession, collection_id: str):

        objs = await db.execute(select(func.count(self.model.status), self.model.status)
                                .group_by(self.model.status)
                                .filter(self.model.collection_id == collection_id))
        return objs

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        obj = await db.scalars(select(self.model).filter_by(id=id, hide=False))
        return obj.first()


application_crud = CRUDApplication(Application)
