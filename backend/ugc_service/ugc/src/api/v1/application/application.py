from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import Depends, Query
from fastapi_pagination import Page
from fastapi_pagination.ext.async_sqlalchemy import paginate as async_paginate

from api.v1.application.base import BaseApplicationAPI, base_error_response
from core.deps import get_moderator
from core.utils import none_or_not_found, validation_schema
from core.utils.cbv import cbv
from core.utils.inferring_router import InferringRouter
from schemas.application import (ApplicationSchema,
                                 FilterSortApplicationSchema,
                                 ModerationApplicationExternalSchema,
                                 ModerationApplicationInnerSchema, StatusCount)
from schemas.auth import User
from models.application import Application, StatusApplicationEnum
from schemas.enums import SortCreatedUpdatedEnum

router = InferringRouter(tags=["applications"], responses=base_error_response)


@cbv(router)
class ApplicationAPI(BaseApplicationAPI):
    user: User = Depends(get_moderator)
    model = Application

    @router.get("/{application_id}", response_model=ApplicationSchema)
    async def get(self, application_id: str):
        """
        Возваращает любую заявку по id
        Права ugc_moderator (admin, superadmin, moderator)
        """
        application = await self.service.get(self.db, obj_id=application_id)
        await none_or_not_found(application)

        return ApplicationSchema.from_orm(application)

    @router.patch("/{application_id}", response_model=ApplicationSchema)
    async def update(self, application_id: str, data: ModerationApplicationExternalSchema):
        """
        Редактирует статусы заявки
        Права ugc_moderator (admin, superadmin, moderator)
        """

        data = data.dict()
        data["moderator_wallet"] = self.user.user_wallet
        data = await validation_schema(ModerationApplicationInnerSchema, data)

        application = await self.service.get(self.db, obj_id=application_id)
        await none_or_not_found(application)

        new_application = await self.service.moderators_update(db=self.db, application=application, update_data=data)

        return ApplicationSchema.from_orm(new_application)

    @router.get("/filter/", response_model=Page[ApplicationSchema])
    async def get_list(
            self,
            collection_id: Optional[List[UUID]] = Query(None, title="ID коллекции"),
            status: Optional[List[StatusApplicationEnum]] = Query(None, title="Статусы"),
            q: Optional[str] = Query(None, title="Поиск по имени в дискорде и кошельку пользователя"),
            created_at_gt: Optional[datetime] = Query(None, title="Дата от "),
            sort: Optional[SortCreatedUpdatedEnum] = None
    ):
        """
        Права ugc_moderator (admin, superadmin, moderator)
        """
        params = {
            'in_values': {},
            'search': {},
            'range_gt': {},
                  }
        if collection_id:
            params['in_values'].update({'collection_id': collection_id})
        if status:
            params['in_values'].update({'status': status})

        if q:
            params['search'].update({'q': q})

        if created_at_gt:
            params['range_gt'].update({'created_at': created_at_gt})

        data = await validation_schema(FilterSortApplicationSchema, params)

        object_list_query = await self.service.get_object_list_query(params=data, sort=sort)
        return await async_paginate(self.db, object_list_query)

    @router.get("/count/{collection_id}", response_model=List[StatusCount])
    async def get_count_list(self, collection_id: str):
        """
        Возвращает список подсчитанных заявок по статусам для коллекции
        """

        status_list = await self.service.get_count_status_by_collection(self.db, collection_id=collection_id)

        return [StatusCount(count=status[0], status=status[1]) for status in status_list]
