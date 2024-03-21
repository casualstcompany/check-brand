from typing import Optional

from fastapi import Depends
from fastapi_pagination import Page
from fastapi_pagination.ext.async_sqlalchemy import paginate as async_paginate

from api.v1.application.base import BaseApplicationAPI
from core import error
from core.deps import get_current_user
from core.utils import none_or_not_found, validation_schema
from core.utils.cbv import cbv
from core.utils.inferring_router import InferringRouter
from grpc_components import admin_grpc_client
from schemas.application import (ApplicationSchema, UserBookApplicationSchema,
                                 UserCreateApplicationExternalSchema,
                                 UserCreateApplicationInnerSchema,
                                 UserEditApplicationExternalSchema,
                                 UserEditApplicationInnerSchema,
                                 UserHideApplicationSchema)
from schemas.auth import User

router = InferringRouter(tags=["user_applications"],)


@cbv(router)
class UserApplicationAPI(BaseApplicationAPI):
    user: User = Depends(get_current_user)

    @router.post("/{collection_id}", response_model=ApplicationSchema)
    async def create(self, collection_id: str, data: UserCreateApplicationExternalSchema):

        new_data = data.dict()
        new_data['user_wallet'] = self.user.user_wallet
        new_data['collection_id'] = collection_id
        obj_in = await validation_schema(UserCreateApplicationInnerSchema, new_data)

        application = await self.service.get_object_by_collection_and_wallet(
            self.db, collection_id, self.user.user_wallet
        )

        collection_json, collection_error = await admin_grpc_client.client.get_collection(collection_id=collection_id)

        if application:
            raise error.BaseError(status_code=400, detail="already exists")

        if collection_error:
            raise error.BaseError(status_code=400, detail="Something went wrong. Please try again later.")

        if not collection_json:
            raise error.BaseError(status_code=400, detail="collection not found")

        new_application = await self.crud.create(db=self.db, obj_in=obj_in)

        return ApplicationSchema.from_orm(new_application)

    @router.get("/{collection_id}", response_model=ApplicationSchema)
    async def get(self, collection_id: str):

        application = await self.service.get_object_by_collection_and_wallet(
            self.db, collection_id, self.user.user_wallet
        )
        await none_or_not_found(application)

        return ApplicationSchema.from_orm(application)

    @router.get("/", response_model=Page[ApplicationSchema])
    async def get_list(self, sort: Optional[str] = None):
        """Возвращает заявки только с бронями"""

        query = await self.service.get_by_wallet_and_token_not_null_query(
            wallet=self.user.user_wallet, sort=sort
        )
        return await async_paginate(self.db, query)

    @router.patch("/edit/{application_id}", response_model=ApplicationSchema)
    async def edit(self, application_id: str, data: UserEditApplicationExternalSchema):

        data = await validation_schema(UserEditApplicationInnerSchema, data.dict())

        application = await self.service.update_users_application(
            db=self.db,
            application_id=application_id,
            user_wallet=self.user.user_wallet,
            data=data
        )
        await none_or_not_found(application)

        return ApplicationSchema.from_orm(application)

    @router.put("/book/{application_id}", response_model=ApplicationSchema)
    async def book(self, application_id: str, data: UserBookApplicationSchema):

        application = await self.service.update_users_application(
            db=self.db,
            application_id=application_id,
            user_wallet=self.user.user_wallet,
            data=data,
            type_update="book"
        )

        await none_or_not_found(application)

        return ApplicationSchema.from_orm(application)

    @router.put("/hide/{application_id}", response_model=ApplicationSchema)
    async def hide(self, application_id: str):
        data = await validation_schema(UserHideApplicationSchema, {"hide": True})

        application = await self.service.update_users_application(
            db=self.db,
            application_id=application_id,
            user_wallet=self.user.user_wallet,
            data=data,
            type_update="hide"
        )
        await none_or_not_found(application)

        return ApplicationSchema.from_orm(application)
