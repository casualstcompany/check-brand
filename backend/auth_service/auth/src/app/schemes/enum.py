from enum import Enum


class SortByUsersRolesEnum(str, Enum):
    desc_created = "-created"
    asc_created = "created"
    desc_updated = "-updated"
    asc_updated = "updated"


class RoleEnum(str, Enum):
    super_admin = "super_admin"
    admin = "admin"
    admin_platform = "admin_platform"
    admin_account = "admin_account"
    admin_collection = "admin_collection"
    owner_collection = "owner_collection"
    moderator_wl = "moderator_wl"
    moderator_list = "moderator_list"
    moderator_store = "moderator_store"
    moderator_factory = "moderator_factory"
    moderator_delivery = "moderator_delivery"
    moderator_opportunity = "moderator_opportunity"
    validator = "validator"
    user = "user"
