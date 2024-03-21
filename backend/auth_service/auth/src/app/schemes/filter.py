from typing import List, Optional
from uuid import UUID

from schemes.base import BaseSchema
from schemes.enum import RoleEnum, SortByUsersRolesEnum


class BaseFilterModel(BaseSchema):
    q: Optional[str] = None
    sort_by: Optional[SortByUsersRolesEnum] = SortByUsersRolesEnum.asc_created
    page: Optional[int] = 1
    page_size: Optional[int] = 10
    account_ids: Optional[List[UUID]] = None
    collection_ids: Optional[List[UUID]] = None
    pack_ids: Optional[List[UUID]] = None
    role_names: Optional[List[RoleEnum]] = None
    wallets: Optional[List[str]] = None
