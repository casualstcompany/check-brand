import logging
from typing import Optional

from sqlalchemy import update, select

from core.deps import ContextManagerAsyncSession
from crud.base import ModelType
from models import Application


class CRUDApplicationGRPC:
    model = Application
    manager = ContextManagerAsyncSession

    async def update_with_filter_by_status_and_collection(self, filter_data: dict, update_data: dict):
        logging.info("Updating")
        logging.info(update_data)
        stmt = (
            update(self.model).
            where(
                self.model.hide == filter_data["hide"],
                self.model.status == filter_data["status"],
                self.model.collection_id == filter_data["collection_id"],
            ).
            values(update_data)
        )

        with self.manager() as db:
            await db.execute(stmt)
            await db.commit()

    async def get_list_by_params(self, params: dict) -> Optional[ModelType]:
        with self.manager() as db:
            obj = await db.scalars(select(self.model).filter_by(**params))
            obj_all = obj.all()
        return obj_all


application_crud_grpc = CRUDApplicationGRPC()

# TODO: при переводе заявок в другие статусы убирать token_id   И ПРИ УДАЛЕНИИ HIDE
