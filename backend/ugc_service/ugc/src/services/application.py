import logging
from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession

from core import error
from core.utils import validation_schema
from crud.application import application_crud
from crud.application_grpc import application_crud_grpc
from crud.base import ModelType
from grpc_components import admin_grpc_client
from models.application import StatusApplicationEnum, Application
from schemas.application import (ApplicationByCollectionSchema,
                                 ApplicationByWallerAndCollectionSchema,
                                 ModerationApplicationInnerSchema, StatusTokenEnum, ApplicationWhiteListResponseSchema)
from schemas.base import BaseSchema, BaseUUIDSchema
from services.base import BaseService
from worker.tasks import task_send_notify_added_white_list, task_send_notify


class ApplicationService(BaseService):
    crud = application_crud
    crud_grpc = application_crud_grpc

    async def get_object_list_query(self, params: BaseSchema, sort: Optional[str] = None):
        query = await self.crud.get_object_list_query(params=params.dict(exclude_none=True), sort=sort)
        return query

    async def get_applications_by_params_for_grpc(self, params: BaseSchema) -> List[ApplicationWhiteListResponseSchema]:
        """Использую для grpc сервиса другой crud, та как там по-особенному идёт обращение к БД."""
        applications = await self.crud_grpc.get_list_by_params(params=params.dict())
        return applications

    async def get_object_by_collection_and_wallet(self, db: AsyncSession, collection_id: str, user_wallet: str):
        data = {"collection_id": collection_id, "user_wallet": user_wallet}
        params = await validation_schema(ApplicationByWallerAndCollectionSchema, data)

        return await self.crud.get_by_params(db=db, params=params.dict())

    async def get_by_collection_and_token_not_null(self, db: AsyncSession, collection_id: str):
        data = {"collection_id": collection_id}
        params = await validation_schema(ApplicationByCollectionSchema, data)

        objs = await self.crud.get_by_collection_and_token_not_null(db=db, collection_id=params.collection_id)
        return objs

    async def get_by_wallet_and_token_not_null_query(self, wallet: str, sort: Optional[str] = None):
        objs = await self.crud.get_by_wallet_and_token_not_null_query(wallet=wallet, sort=sort)
        return objs

    async def update_users_application(self, db: AsyncSession, application_id: str,
                                       user_wallet: str, data: BaseSchema, type_update: str = None):
        field_none = []
        token = None

        await validation_schema(BaseUUIDSchema, {"id": application_id})

        application = await self.get(db=db, obj_id=application_id)

        if application is None or application.user_wallet != user_wallet:
            return None

        if type_update == "book":
            token = await self.validate_book(db=db, application=application, token_id=str(data.token_id))

        if type_update == "hide":
            data.token_id = None
            field_none = ["token_id"]

        new_application = await self.crud.update(db=db, db_obj=application, update_data=data, field_none=field_none)

        if type_update == "book" and token:
            logging.debug("user_booked")
            task_send_notify.delay(payload={
                    "collection_id": str(token.collection),
                    "token_id": str(token.id),
                    "token_name": token.name,
                    "token_file_url": token.file_1,
                    "user_wallet": application.user_wallet,
                    "email": [application.email, ]
                },
                content_type="user_booked", get_collection=True)

        return new_application

    async def get_count_status_by_collection(self, db: AsyncSession, collection_id: str):
        """ Возвращает подсчитанные count по статусам """
        await validation_schema(BaseUUIDSchema, {"id": collection_id})
        return await self.crud.get_count_status_by_collection(db=db, collection_id=collection_id)

    async def moderators_update(self, db: AsyncSession, application: ModelType,
                                update_data: ModerationApplicationInnerSchema) -> ModelType:
        """
            Модератор может перевести заявку в следующие статусы:
            white - в этом случае оповещаем пользователя
            read, new - ничего не делаем.

            Может убрать у пользователя бронь на (token_id=null)
            field_none=["token_id"] - указывает на то, что при null тоже перезаписывать поле.
        """
        field_none = []
        list_status = [StatusApplicationEnum.read.value, StatusApplicationEnum.new.value]
        need_notify_user = False

        if update_data.token_none:
            field_none = ["token_id"]

        if update_data.status in list_status:
            update_data.token_id = None
            field_none = ["token_id"]

        if update_data.status == StatusApplicationEnum.white and application.status in list_status:
            need_notify_user = True
            update_data.in_work = False

        obj = await self.crud.update(db=db, db_obj=application, update_data=update_data, field_none=field_none)

        if need_notify_user:
            logging.debug("read or new --> white")
            payload = {
                "collection_id": str(application.collection_id),
                "user_wallet": application.user_wallet,
                "email": [application.email, ]
            }
            task_send_notify_added_white_list.delay(payload=payload)
        return obj

    async def validate_book(self, db: AsyncSession, application: Application, token_id: str):

        token, token_error = await admin_grpc_client.client.get_token(token_id)

        if application.status != StatusApplicationEnum.white:
            raise error.BaseError(status_code=400, detail="must be whitelisted")

        if application.token_id is not None:
            raise error.BaseError(status_code=400, detail="One booking available in the collection")

        params = {"token_id": token_id, "hide": False}

        if await self.crud.get_by_params(db=db, params=params):
            raise error.BaseError(status_code=400, detail="token already booked")

        if token_error:
            raise error.BaseError(status_code=400, detail="Something went wrong. Please try again later.")

        # TODO: тут мб надо буде проверять по  collection.status
        if not token or token and (token.status_price != "price"
                                   or float(token.price) == 0 or token.price == None
                                   or token.status != "book" or token.mint == True):

            raise error.BaseError(status_code=400, detail="unable to reserve a specific token")

        if token.collection != str(application.collection_id):
            raise error.BaseError(status_code=400, detail="the token is not in the collection specified in the leaf")

        return token

    async def update_applications_by_status_tokens(self, status_token: str, collection_id: str):

        filter_data = {
            "hide": False,
            "status": StatusApplicationEnum.white.value,
            "collection_id": collection_id,
        }
        update_data = {}

        if status_token in [StatusTokenEnum.stop, StatusTokenEnum.sold_out, StatusTokenEnum.mint_2]:
            update_data.update({"token_id": None})

        if status_token in [StatusTokenEnum.stop, StatusTokenEnum.sold_out]:
            update_data.update({"status": StatusApplicationEnum.read.value})

        await self.crud_grpc.update_with_filter_by_status_and_collection(
            filter_data=filter_data, update_data=update_data
        )


application_service = ApplicationService()
