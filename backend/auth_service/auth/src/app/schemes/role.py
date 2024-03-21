from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import validator
from schemes.base import BaseSchema
from schemes.resource_access import (
    CreateUpdateResourceAccessSchema,
    ResourceAccessSchema,
)
from schemes.user import Profile


class Role(BaseSchema):
    name: str
    public_name: str


class RolesUsersSchema(BaseSchema):
    id: UUID
    user_profile: Profile
    creator_profile: Optional[Profile]
    role: Role
    description: Optional[str]
    access: List[ResourceAccessSchema] = []

    created: datetime = None
    updated: datetime = None


class CreateRolesUsersSchema(BaseSchema):
    public_address: str
    description: Optional[str]
    role_number: int
    access: List[Optional[CreateUpdateResourceAccessSchema]] = []

    @validator("public_address", pre=True)
    def validate_public_address(cls, v):
        """Приведем к нижнему регистру"""
        return v.lower()


class UpdateRolesUsersSchema(BaseSchema):
    description: Optional[str]
    access: List[Optional[CreateUpdateResourceAccessSchema]] = []
    remove_access: List[Optional[UUID]] = []


class UserAccessSchema(BaseSchema):
    accounts: List[Optional[UUID]] = []
    collections: List[Optional[UUID]] = []
    packs: List[Optional[UUID]] = []


class UserPermissionsAccessSchema(BaseSchema):
    public_address: Optional[str]
    permissions: List[Optional[str]] = []
    access: UserAccessSchema = UserAccessSchema()


class PageRolesUsersSchema(BaseSchema):
    count: int = 0
    total_pages: int = 0
    page: int = 1
    page_size: int = 10
    results: List[Optional[RolesUsersSchema]] = []
