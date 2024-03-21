from schemes import BaseFilterModel, ErrorResponseSchema, SortByUsersRolesEnum
from schemes.role import (
    CreateRolesUsersSchema,
    PageRolesUsersSchema,
    RolesUsersSchema,
    UpdateRolesUsersSchema,
    UserPermissionsAccessSchema,
)

RESPONSES = {
    401: {
        "description": "UNAUTHORIZED",
        "examples": {
            "application/json": {"msg": "Missing Authorization Header"}
        },
    },
    400: {
        "description": "BAD REQUEST",
        "schema": {"$ref": "#/definitions/ErrorResponseSchema"},
    },
}


def create_swag_users_roles():
    users_roles = {
        "tags": ["UsersRoles"],
        "summary": "Общая структура",
        "security": [{"Bearer": []}],
        "consumes": ["application/json"],
        "produces": ["application/json"],
        "responses": {
            "200": {
                "description": "OK",
                "schema": {"$ref": "#/definitions/RolesUsersSchema"},
            },
            "401": RESPONSES.get(401),
            "400": RESPONSES.get(400),
        },
        "definitions": {
            "CreateRolesUsersSchema": CreateRolesUsersSchema.schema(),
            "ErrorResponseSchema": ErrorResponseSchema.schema(),
            "RolesUsersSchema": RolesUsersSchema.schema(),
            "UpdateRolesUsersSchema": UpdateRolesUsersSchema.schema(),
            "BaseFilterModel": BaseFilterModel.schema(),
            "PageRolesUsersSchema": PageRolesUsersSchema.schema(),
            "UserPermissionsAccessSchema": (
                UserPermissionsAccessSchema.schema()
            ),
        },
        "parameters": [
            {
                "in": "path",
                "name": "users_roles_id",
                "description": "Идентификатор роли пользователя",
                "type": "string",
            },
        ],
    }
    _get_list_users_roles = users_roles.copy()
    _get_user_permissions_and_access = users_roles.copy()
    _create_users_roles = users_roles.copy()
    _get_users_roles = users_roles.copy()
    _update_users_roles = users_roles.copy()
    _delete_users_roles = users_roles.copy()

    _create_users_roles.update(
        {
            "summary": (
                "Создает роль пользователю с доступами к определенным ресурсам"
            ),
            "operationId": "CreateUserAccessPermissions",
            "parameters": [
                {
                    "in": "body",
                    "name": "body",
                    "description": "Данные для создания роли",
                    "schema": {"$ref": "#/definitions/CreateRolesUsersSchema"},
                }
            ],
        }
    )

    _update_users_roles.update(
        {
            "summary": (
                "Редактирует роль пользователю с доступами к определенным"
                " ресурсам"
            ),
            "operationId": "UpdateUserAccessPermissions",
            "parameters": [
                {
                    "in": "path",
                    "name": "users_roles_id",
                    "description": "Идентификатор роли пользователя",
                    "type": "string",
                },
                {
                    "in": "body",
                    "name": "body",
                    "description": "Данные для редактирования роли",
                    "schema": {"$ref": "#/definitions/UpdateRolesUsersSchema"},
                },
            ],
        }
    )
    _delete_users_roles.update(
        {
            "summary": (
                "Удаляет полностью роль пользователю с доступами к"
                " определенным ресурсам"
            ),
            "operationId": "DeleteUserAccessPermissions",
        }
    )
    _get_users_roles.update(
        {
            "summary": (
                "Возвращает роль пользователю с доступами к определенным"
                " ресурсам"
            ),
            "operationId": "GetUserAccessPermissions",
        }
    )

    _get_list_users_roles.update(
        {
            "summary": "Возвращает список ролей пользователей.",
            "operationId": "UsersRolesGetList",
            "parameters": [
                {
                    "in": "query",
                    "name": "q",
                    "description": "Поиск по username",
                    "type": "string",
                },
                {
                    "in": "query",
                    "name": "sort_by",
                    "description": "Сортировка по",
                    "type": "string",
                    "enum": [s.value for s in SortByUsersRolesEnum],
                },
                {
                    "in": "query",
                    "name": "page",
                    "description": "Номер страницы",
                    "type": "integer",
                },
                {
                    "in": "query",
                    "name": "page_size",
                    "description": "Размер страницы",
                    "type": "integer",
                },
                {
                    "in": "query",
                    "name": "account_ids",
                    "description": "Список брендов",
                    "type": "array",
                    "items": {"type": "string", "format": "uuid"},
                },
                {
                    "in": "query",
                    "name": "collection_ids",
                    "description": "Список коллекций",
                    "type": "array",
                    "items": {"type": "string", "format": "uuid"},
                },
                {
                    "in": "query",
                    "name": "pack_ids",
                    "description": "Список паков",
                    "type": "array",
                    "items": {"type": "string", "format": "uuid"},
                },
                {
                    "in": "query",
                    "name": "role_names",
                    "description": "Список имен ролей",
                    "type": "array",
                    "items": {"type": "string"},
                },
                {
                    "in": "query",
                    "name": "wallets",
                    "description": "Список кошельков пользователей",
                    "type": "array",
                    "items": {"type": "string"},
                },
            ],
            "responses": {
                "200": {
                    "description": "OK",
                    "schema": {"$ref": "#/definitions/PageRolesUsersSchema"},
                },
                "401": RESPONSES.get(401),
            },
        }
    )

    _get_user_permissions_and_access.update(
        {
            "summary": (
                "Возвращает список прав доступа пользователя и связанных с"
                " ними объектов."
            ),
            "operationId": "UsersRolesGetUserAccessPermissions",
            "parameters": [],
            "responses": {
                "200": {
                    "description": "OK",
                    "schema": {
                        "$ref": "#/definitions/UserPermissionsAccessSchema"
                    },
                },
                "401": RESPONSES.get(401),
                "400": RESPONSES.get(400),
            },
        }
    )

    return (
        _create_users_roles,
        _get_users_roles,
        _update_users_roles,
        _delete_users_roles,
        _get_user_permissions_and_access,
        _get_list_users_roles,
    )


(
    create_users_roles,
    get_users_roles,
    update_users_roles,
    delete_users_roles,
    get_user_permissions_and_access,
    get_list_users_roles,
) = create_swag_users_roles()
