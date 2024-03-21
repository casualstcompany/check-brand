from typing import Optional
from uuid import UUID

from schemes.base import BaseSchema


class ResourceAccessSchema(BaseSchema):
    id: UUID
    role_user_id: UUID
    resource_id: UUID
    sub_resource_id: Optional[UUID]
    sub_sub_resource_id: Optional[UUID]


class CreateUpdateResourceAccessSchema(BaseSchema):
    resource_id: UUID
    sub_resource_id: Optional[UUID]
    sub_sub_resource_id: Optional[UUID]
