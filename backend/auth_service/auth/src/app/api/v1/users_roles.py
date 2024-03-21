import math
from http import HTTPStatus

from api.v1.response_code import get_error_response as error_response
from api.v1.swag import users_roles as swag
from components.permissions import (
    permissions_create_role,
    permissions_delete_role,
    permissions_update_role,
)
from flasgger import swag_from
from flask import Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_pydantic import validate
from schemes import BaseFilterModel
from schemes.role import (
    CreateRolesUsersSchema,
    PageRolesUsersSchema,
    RolesUsersSchema,
    UpdateRolesUsersSchema,
    UserPermissionsAccessSchema,
)
from services.users_roles import users_roles_service
from utils.check_allowed import validate_uuid4

users_roles = Blueprint("users_roles", __name__)


@users_roles.get("/my")
@jwt_required()
@swag_from(swag.get_user_permissions_and_access)
def get_user_permissions_and_access():
    public_address = get_jwt_identity()

    result = users_roles_service.get_user_permissions_and_access(
        public_address=public_address
    )

    return UserPermissionsAccessSchema.from_orm(result).dict()


@users_roles.get("")
@jwt_required()
@validate()
@swag_from(swag.get_list_users_roles)
def get_list_users_roles(query: BaseFilterModel):
    results = users_roles_service.get_list_users_roles(query_params=query)

    result = PageRolesUsersSchema(
        count=results.total,
        total_pages=math.ceil(results.total / query.page_size),
        page=query.page,
        page_size=query.page_size,
        results=[
            RolesUsersSchema.from_orm(result).dict() for result in results
        ],
    )
    return result


@users_roles.post("")
@jwt_required()
@validate()
@permissions_create_role()
@swag_from(swag.create_users_roles)
def create_users_roles(body: CreateRolesUsersSchema):
    creator_wallet = get_jwt_identity()

    result = users_roles_service.create_users_roles(
        body=body, creator_wallet=creator_wallet
    )

    return RolesUsersSchema.from_orm(result).dict()


@users_roles.delete("/<users_roles_id>")
@jwt_required()
@permissions_delete_role()
@swag_from(swag.delete_users_roles)
def delete_users_roles(users_roles_id):
    if not validate_uuid4(users_roles_id):
        return error_response.fail(
            "Invalid ID", status_code=HTTPStatus.BAD_REQUEST
        )

    result = users_roles_service.delete_users_roles(users_roles_id)

    return RolesUsersSchema.from_orm(result).dict()


@users_roles.get("/<users_roles_id>")
@jwt_required()
@swag_from(swag.get_users_roles)
def get_users_roles(users_roles_id):
    if not validate_uuid4(users_roles_id):
        return error_response.fail(
            "Invalid ID", status_code=HTTPStatus.BAD_REQUEST
        )

    result = users_roles_service.get_users_roles(users_roles_id)

    return RolesUsersSchema.from_orm(result).dict()


@users_roles.patch("/<users_roles_id>")
@jwt_required()
@validate()
@permissions_update_role()
@swag_from(swag.update_users_roles)
def update_users_roles(users_roles_id, body: UpdateRolesUsersSchema):
    creator_wallet = get_jwt_identity()

    result = users_roles_service.update_users_roles(
        body=body, users_roles_id=users_roles_id, creator_wallet=creator_wallet
    )

    return RolesUsersSchema.from_orm(result).dict()
