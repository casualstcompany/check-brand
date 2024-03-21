add_user = {
    "tags": ["Profile"],
    "summary": "Профиль. Добавление/Изменение изображения пользователя",
    "security": [{"Bearer": []}],
    "consumes": ["multipart/form-data"],
    "parameters": [
        {
            "in": "formData",
            "name": "image",
            "description": "Изображение пользователя",
            "type": "file",
        }
    ],
    "produces": ["application/json"],
    "operationId": "ProfileAddImage",
    "responses": {
        "200": {
            "description": "OK",
            "examples": {
                "application/json": {
                    "image_url": (
                        "http://localhost:5000/profile/media/rauha_ava.png"
                    )
                }
            },
        },
        "400": {
            "description": "BAD REQUEST",
            "examples": {
                "application/json": {
                    "data": {"image": ["Field may not be null."]},
                    "msg": "The data is incorrect",
                    "status": "error",
                },
            },
        },
        "401": {
            "description": "UNAUTHORIZED",
            "examples": {"application/json": {"msg": "authentication error"}},
        },
        "413": {
            "description": "REQUEST ENTITY TOO LARGE",
            "examples": {
                "application/json": {
                    "msg": (
                        "The data value transmitted exceeds the capacity"
                        " limit."
                    )
                }
            },
        },
    },
}

profile = {
    "tags": ["Profile"],
    "summary": "Профиль. Информация о пользователе",
    "security": [{"Bearer": []}],
    "consumes": ["multipart/form-data"],
    "parameters": [
        {
            "in": "path",
            "name": "public_address",
            "description": "Публичный ключ",
            "required": True,
        }
    ],
    "produces": ["application/json"],
    "operationId": "ProfileUser",
    "responses": {
        "200": {
            "description": "OK",
            "examples": {
                "application/json": {
                    "id": "0ff68b7e-0d57-4135-bbc9-6771c0dd83f9",
                    "image_url": (
                        "http://localhost/profile/media/rauha_youtube.png"
                    ),
                    "public_address": (
                        "0x45BCD9a9C4C8Ebd2D8c7d9Dba8107A6dD47768FA"
                    ),
                    "username": "cazkgnay",
                    "email": "example@example.com",
                    "email_verified": True,
                }
            },
        },
        "404": {
            "description": "NOT FOUND",
            "examples": {"application/json": {"msg": "authentication error"}},
        },
    },
}

my_profile = {
    "tags": ["Profile"],
    "summary": "Профиль. Информация об авторизованном пользователе",
    "security": [{"Bearer": []}],
    "produces": ["application/json"],
    "operationId": "ProfileMyUser",
    "responses": {
        "200": {
            "description": "OK",
            "examples": {
                "application/json": {
                    "id": "0ff68b7e-0d57-4135-bbc9-6771c0dd83f9",
                    "image_url": (
                        "http://localhost/profile/media/rauha_youtube.png"
                    ),
                    "public_address": (
                        "0x45BCD9a9C4C8Ebd2D8c7d9Dba8107A6dD47768FA"
                    ),
                    "username": "cazkgnay",
                    "email": "example@example.com",
                    "email_verified": True,
                }
            },
        },
        "404": {
            "description": "NOT FOUND",
            "examples": {"application/json": {"msg": "authentication error"}},
        },
        "401": {
            "description": "UNAUTHORIZED",
            "examples": {"application/json": {"msg": "authentication error"}},
        },
    },
}


my_profile_update = {
    "tags": ["Profile"],
    "summary": "Профиль. редактировать личную информацию",
    "security": [{"Bearer": []}],
    "consumes": ["application/json"],
    "parameters": [
        {
            "in": "body",
            "name": "data",
            "description": "Редактировать username, email",
            "schema": {"$ref": "#/definitions/UpdateUserScheme"},
        }
    ],
    "produces": ["application/json"],
    "operationId": "ProfileMyUserUpdate",
    "responses": {
        "200": {
            "description": "OK",
            "examples": {
                "application/json": {
                    "id": "0ff68b7e-0d57-4135-bbc9-6771c0dd83f9",
                    "image_url": (
                        "http://localhost/profile/media/rauha_youtube.png"
                    ),
                    "public_address": (
                        "0x45BCD9a9C4C8Ebd2D8c7d9Dba8107A6dD47768FA"
                    ),
                    "username": "cazkgnay",
                    "email": "example@example.com",
                    "email_verified": False,
                    "telegram": "https://t.me/1111",
                    "whatsapp": "8 800 888 88 88",
                    "instagram": "@insta",
                }
            },
        },
        "404": {
            "description": "NOT FOUND",
            "examples": {"application/json": {"msg": "authentication error"}},
        },
        "401": {
            "description": "UNAUTHORIZED",
            "examples": {"application/json": {"msg": "authentication error"}},
        },
        "400": {
            "description": "BAD REQUEST",
            "examples": {
                "application/json": {
                    "data": {"username": ["Field may not be null."]},
                    "msg": "The data is incorrect",
                    "status": "error",
                },
            },
        },
    },
    "definitions": {
        "UpdateUserScheme": {
            "type": "object",
            "required": ["username"],
            "properties": {
                "username": {"type": "string", "default": "babaklava"},
                "email": {"type": "string", "default": "example@mail.com"},
                "telegram": {"type": "string", "default": "https://t.me/example"},
                "whatsapp": {"type": "string", "default": "88008887766"},
                "instagram": {"type": "string", "default": "example_inst"},
            },
        }
    },
}

confirm_email = {
    "tags": ["Profile"],
    "summary": "Профиль. Подтверждение почты",
    "security": [{"Bearer": []}],
    "consumes": ["multipart/form-data"],
    "parameters": [
        {
            "in": "path",
            "name": "otp_code",
            "description": "Код подтверждения",
            "required": True,
        }
    ],
    "produces": ["application/json"],
    "operationId": "ProfileUserConfirmEmail",
    "responses": {
        "200": {
            "description": "OK",
            "examples": {
                "application/json": {
                    "status": "success",
                }
            },
        },
        "404": {
            "description": "NOT FOUND",
            "examples": {"application/json": {"msg": "authentication error"}},
        },
    },
}