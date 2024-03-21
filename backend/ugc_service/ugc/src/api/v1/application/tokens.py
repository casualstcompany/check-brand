from fastapi import Depends

from api.v1.application.base import BaseApplicationAPI
from core.auth import JWTBearer
from core.utils.cbv import cbv
from core.utils.inferring_router import InferringRouter
from schemas.application import TokenApplicationSchema
from schemas.token import TokenListSchema

router = InferringRouter(tags=["tokens_applications"], dependencies=[Depends(JWTBearer())])


@cbv(router)
class ApplicationAPI(BaseApplicationAPI):

    @router.post("/", response_model=TokenListSchema)
    async def get_tokens_in_applications(self, data: TokenListSchema):
        """
        Возвращает из полученного списка токенов только те токены
        которые есть в активных заявках
        """
        applications = await self.crud.get_by_list_token(db=self.db, data=data)

        return TokenListSchema(
            tokens=[TokenApplicationSchema.from_orm(application).token_id for application in applications]
        )

    @router.post("/{collection_id}", response_model=TokenListSchema)
    async def get_tokens_in_applications_by_collection(self, collection_id: str):
        """
        Возвращает все токены которые есть в активных заявках
        по указанной коллекции
        """
        # TODO: поменять метод на GET и сказать об этом фронту

        applications = await self.service.get_by_collection_and_token_not_null(db=self.db, collection_id=collection_id)

        return TokenListSchema(
            tokens=[TokenApplicationSchema.from_orm(application).token_id for application in applications]
        )
