from flasgger import Swagger

template = {
    "swagger": "2.0",
    "info": {
        "title": "Сервис авторизации",
        "description": "",
        "version": "0.1.0",
        "contact": {
            "name": "CheckBrand",
            "url": "http://localhost:5000",  # TODO: вынести в конфиг
        },
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": (
                "Авторизация JWT с использованием схемы Bearer. Пример:"
                ' "Authorization: Bearer {token}"'
            ),
        }
    },
}

swagger = Swagger(template=template)
