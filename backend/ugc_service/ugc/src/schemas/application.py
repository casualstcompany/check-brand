import enum
from datetime import datetime
from typing import Optional, List, Dict
from uuid import UUID

from pydantic import EmailStr

from models.application import StatusApplicationEnum
from schemas.base import BaseSchema


class ApplicationSchema(BaseSchema):
    id: UUID
    collection_id: UUID
    token_id: UUID = None
    status: StatusApplicationEnum
    user_wallet: str
    discord_name: str
    email: EmailStr
    field_1: Optional[str]
    field_2: Optional[str]
    field_3: Optional[str]
    field_4: Optional[str]
    field_5: Optional[str]
    field_6: Optional[str]
    field_7: Optional[str]
    field_8: Optional[str]
    field_9: Optional[str]
    field_10: Optional[str]
    description: Optional[str]
    number: int = 0
    moderator_wallet: Optional[str] = None
    in_work: bool
    hide: bool
    created_at: datetime
    updated_at: datetime = None


class ApplicationByWallerAndCollectionSchema(BaseSchema):
    collection_id: UUID
    user_wallet: str
    hide: bool = False


class ApplicationByCollectionSchema(BaseSchema):
    collection_id: Optional[UUID] = None
    hide: bool = False


class InFilterSortApplicationSchema(BaseSchema):
    collection_id: Optional[List[UUID]]
    status: Optional[List[StatusApplicationEnum]]


class SearchFilterSortApplicationSchema(BaseSchema):
    q: Optional[str]
    search_fields = ['user_wallet', 'discord_name']


class RangeGtFilterSortApplicationSchema(BaseSchema):
    created_at: Optional[datetime]


class FilterSortApplicationSchema(BaseSchema):
    in_values: InFilterSortApplicationSchema
    search: SearchFilterSortApplicationSchema
    range_gt: RangeGtFilterSortApplicationSchema


class StatusCount(BaseSchema):
    count: int
    status: StatusApplicationEnum


class ModerationApplicationExternalSchema(BaseSchema):
    status: Optional[StatusApplicationEnum]
    in_work: Optional[bool]
    token_id: Optional[UUID]  # TODO: как на фронте уберем, тут тоже убрать
    token_none: bool = False


class ModerationApplicationInnerSchema(BaseSchema):
    status: Optional[StatusApplicationEnum]
    in_work: Optional[bool]
    token_id: Optional[UUID]  # TODO: как на фронте уберем, тут тоже убрать
    moderator_wallet: str
    token_none: bool = False


class UserApplicationBaseSchema(BaseSchema):
    field_1: Optional[str]
    field_2: Optional[str]
    field_3: Optional[str]
    field_4: Optional[str]
    field_5: Optional[str]
    field_6: Optional[str]
    field_7: Optional[str]
    field_8: Optional[str]
    field_9: Optional[str]
    field_10: Optional[str]
    description: Optional[str]
    discord_name: str
    email: EmailStr


class UserCreateApplicationExternalSchema(UserApplicationBaseSchema):
    pass


class UserEditApplicationExternalSchema(UserApplicationBaseSchema):
    pass


class UserEditApplicationInnerSchema(UserApplicationBaseSchema):
    status: StatusApplicationEnum = StatusApplicationEnum.new


class UserCreateApplicationInnerSchema(UserApplicationBaseSchema):
    collection_id: UUID
    user_wallet: str


class UserBookApplicationSchema(BaseSchema):
    token_id: UUID


class TokenApplicationSchema(BaseSchema):
    token_id: UUID


class UserHideApplicationSchema(BaseSchema):
    hide: bool
    token_id: Optional[UUID]


class StatusTokenEnum(str, enum.Enum):
    mint_2 = "mint_2"
    stop = "stop"
    sold_out = "sold_out"


class UpdateApplicationByStatusRequestSchema(BaseSchema):
    status_token: StatusTokenEnum
    collection_id: UUID


class ListApplicationWhiteListRequestSchema(BaseSchema):
    hide: bool = False
    collection_id: UUID
    status: StatusApplicationEnum = StatusApplicationEnum.white


class ApplicationWhiteListResponseSchema(BaseSchema):
    id: str
    user_wallet: str
    email: EmailStr
