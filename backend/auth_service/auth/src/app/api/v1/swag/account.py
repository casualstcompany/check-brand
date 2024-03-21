get_nonce = {
    "tags": ["Web3Auth"],
    "summary": "Авторизация. Получение nonce",
    "parameters": [
        {
            "in": "query",
            "name": "public_address",
            "description": "Публичный ключ",
        }
    ],
    "produces": ["application/json"],
    "operationId": "Web3Nonce",
    "responses": {
        "200": {
            "description": "OK",
            "examples": {
                "application/json": {
                    "nonce": "12345",
                }
            },
        },
        "400": {
            "description": "OK",
            "examples": {
                "application/json": {
                    "data": {"public_address": ["Unknown field."]},
                    "msg": "The data is incorrect",
                    "status": "error",
                }
            },
        },
    },
}

authentication = {
    "tags": ["Web3Auth"],
    "summary": "Авторизация. Подтверждение кошелька",
    "consumes": ["application/json"],
    "parameters": [
        {
            "in": "body",
            "name": "data",
            "description": (
                "Данные после подписи в MetaMask('I am signing my one-time"
                " nonce:12345')"
            ),
            "schema": {"$ref": "#/definitions/PublicAndSignatureScheme"},
        }
    ],
    "produces": ["application/json"],
    "operationId": "Web3Signature",
    "responses": {
        "200": {
            "description": "OK",
            "examples": {
                "application/json": {
                    "access_token": "eyJ0eX........-3T8JB9M",
                    "refresh_token": "eyJ0eXA.......a3BUbVpP0Q-_PHI",
                }
            },
        },
        "400": {
            "description": "OK",
            "examples": {
                "application/json": {
                    "data": {
                        "public_address": ["Field may not be null."],
                        "signature": ["Field may not be null."],
                    },
                    "msg": "The data is incorrect",
                    "status": "error",
                }
            },
        },
        "401": {
            "description": "UNAUTHORIZED",
            "examples": {"application/json": {"msg": "authentication error"}},
        },
    },
    "definitions": {
        "PublicAndSignatureScheme": {
            "type": "object",
            "required": ["public_address", "signature"],
            "properties": {
                "public_address": {
                    "type": "string",
                    "default": "0x45BCD9a9C4C8Ebd2D8c7d9Dba8107A6dD47768FA",
                },
                "signature": {
                    "type": "string",
                    "default": (
                        "0x06585a9172861bb98d0.....605c06f3daf590d67e2b1c"
                    ),
                },
            },
        }
    },
}

refresh = {
    "tags": ["Web3Auth"],
    "summary": "Получение нового refresh токена",
    "description": "Необходимо авторизрвываться через refresh",
    "security": [{"Bearer": []}],
    "produces": ["application/json"],
    "operationId": "Web3Refresh",
    "responses": {
        "200": {
            "description": "OK",
            "examples": {
                "application/json": {
                    "access_token": "eyJ0eX........-3T8JB9M",
                    "refresh_token": "eyJ0eXA.......a3BUbVpP0Q-_PHI",
                }
            },
        },
        "401": {
            "description": "UNAUTHORIZED",
            "examples": {"application/json": {"msg": "authentication error"}},
        },
        "422": {
            "description": "Error: UNPROCESSABLE ENTITY",
            "examples": {
                "application/json": {"msg": "Only refresh tokens are allowed"}
            },
        },
    },
}

logout = {
    "tags": ["Web3Auth"],
    "summary": "Выход",
    "security": [{"Bearer": []}],
    "produces": ["application/json"],
    "operationId": "Web3Logout",
    "responses": {
        "200": {
            "description": "OK",
            "examples": {"application/json": {"msg": "success logout"}},
        },
        "401": {
            "description": "UNAUTHORIZED",
            "examples": {"application/json": {"msg": "authentication error"}},
        },
    },
}
full_logout = {
    "tags": ["Web3Auth"],
    "summary": "Выход со всех браузеров(устройств)",
    "security": [{"Bearer": []}],
    "produces": ["application/json"],
    "operationId": "Web3FullLogout",
    "responses": {
        "200": {
            "description": "OK",
            "examples": {"application/json": {"msg": "success logout"}},
        },
        "401": {
            "description": "UNAUTHORIZED",
            "examples": {"application/json": {"msg": "authentication error"}},
        },
    },
}
