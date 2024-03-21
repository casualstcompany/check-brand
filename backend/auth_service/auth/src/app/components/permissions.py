from functools import wraps
from http import HTTPStatus

from api.v1.response_code import get_error_response as error_response
from flask_jwt_extended import get_jwt_identity
from schemes import RoleEnum
from services.role import role_service
from services.users_roles import users_roles_service
from utils.check_allowed import validate_uuid4


def _validate_allowed_user_on_create_update_roles(
    user_permissions_and_access, role, list_access, type_str
):
    if f"{type_str}_{role.name}" in user_permissions_and_access.permissions:
        return True

    if f"{type_str}_{role.name}_in" in user_permissions_and_access.permissions:
        for access in list_access:
            if role.name in [RoleEnum.admin_collection]:
                if (
                    str(access.resource_id)
                    not in user_permissions_and_access.access["accounts"]
                ):
                    return False
            elif role.name in [
                RoleEnum.moderator_wl,
                RoleEnum.moderator_list,
                RoleEnum.moderator_store,
                RoleEnum.moderator_factory,
                RoleEnum.moderator_delivery,
                RoleEnum.moderator_opportunity,
                RoleEnum.validator,
            ]:
                if (
                    str(access.sub_resource_id)
                    not in user_permissions_and_access.access["collections"]
                    and str(access.resource_id)
                    not in user_permissions_and_access.access["accounts"]
                ):
                    return False
        return True

    return False


def permissions_create_role():
    def wrapper(func):
        @wraps(func)
        def decorate_view(*args, **kwargs):
            body = kwargs.get("body")
            role = role_service.get_role_by_number(
                role_number=body.role_number
            )

            if not role:
                return error_response.fail(
                    "Role not found", status_code=HTTPStatus.BAD_REQUEST
                )

            user_permissions_and_access = (
                users_roles_service.get_user_permissions_and_access(
                    public_address=get_jwt_identity()
                )
            )

            if user_permissions_and_access:
                if _validate_allowed_user_on_create_update_roles(
                    user_permissions_and_access, role, body.access, "create"
                ):
                    return func(*args, **kwargs)

            return error_response.fail(
                "You don't have enough rights",
                status_code=HTTPStatus.FORBIDDEN,
            )

        return decorate_view

    return wrapper


def permissions_update_role():
    def wrapper(func):
        @wraps(func)
        def decorate_view(*args, **kwargs):
            users_roles_id = kwargs.get("users_roles_id")
            body = kwargs.get("body")

            if not validate_uuid4(users_roles_id):
                return error_response.fail(
                    "Invalid ID", status_code=HTTPStatus.BAD_REQUEST
                )

            users_roles = users_roles_service.get_users_roles(
                users_roles_id=users_roles_id
            )

            user_permissions_and_access = (
                users_roles_service.get_user_permissions_and_access(
                    public_address=get_jwt_identity()
                )
            )

            if user_permissions_and_access:
                list_resource_access = []
                if body.remove_access:
                    list_resource_access = users_roles_service.get_list_resource_access_by_roles_users_id_and_list_id(
                        roles_users_id=users_roles_id,
                        list_id=body.remove_access,
                    )

                if _validate_allowed_user_on_create_update_roles(
                    user_permissions_and_access,
                    users_roles.role,
                    body.access + list_resource_access,
                    "update",
                ):
                    return func(*args, **kwargs)

            return error_response.fail(
                "You don't have enough rights",
                status_code=HTTPStatus.FORBIDDEN,
            )

        return decorate_view

    return wrapper


def permissions_delete_role():
    def wrapper(func):
        @wraps(func)
        def decorate_view(*args, **kwargs):
            users_roles_id = kwargs.get("users_roles_id")

            if not validate_uuid4(users_roles_id):
                return error_response.fail(
                    "Invalid ID", status_code=HTTPStatus.BAD_REQUEST
                )

            users_roles = users_roles_service.get_users_roles(
                users_roles_id=users_roles_id
            )

            user_permissions_and_access = (
                users_roles_service.get_user_permissions_and_access(
                    public_address=get_jwt_identity()
                )
            )

            if user_permissions_and_access:
                if _validate_allowed_user_on_create_update_roles(
                    user_permissions_and_access,
                    users_roles.role,
                    users_roles.access,
                    "delete",
                ):
                    return func(*args, **kwargs)

            return error_response.fail(
                "You don't have enough rights",
                status_code=HTTPStatus.FORBIDDEN,
            )

        return decorate_view

    return wrapper


def permissions_get_personal_role():
    """Пока не используется, дабы избегаем лишнего запроса"""

    def wrapper(func):
        @wraps(func)
        def decorate_view(*args, **kwargs):
            user_permissions_and_access = (
                users_roles_service.get_user_permissions_and_access(
                    public_address=get_jwt_identity()
                )
            )

            if (
                user_permissions_and_access
                and "get_personal" in user_permissions_and_access.permissions
            ):
                return func(*args, **kwargs)

            return error_response.fail(
                "You don't have enough rights",
                status_code=HTTPStatus.FORBIDDEN,
            )

        return decorate_view

    return wrapper
