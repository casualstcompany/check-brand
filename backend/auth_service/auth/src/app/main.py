import logging
from pydoc import locate

from api import v1
from api.v1.response_code import bp_errors
from components import admin_grpc_client
from components.datastore import datastore
from components.error import handle_exception
from config.config import config
from config.swagger import swagger
from config.utils import init_db, init_ma
from extension import jwt, security
from flask import Flask
from middlewares import init_token_check
from models import *
from werkzeug.exceptions import HTTPException

admin_grpc_client_cls = locate(config.ADMIN_GRPC.CLS)


def configure_logger(app: Flask) -> None:
    app.logger = logging.getLogger(__name__)
    app.logger.setLevel(logging.INFO)


def configure_blueprints(app: Flask) -> None:
    app.register_blueprint(
        v1.users_roles, url_prefix="/auth_service/api/v1/users_roles/"
    )
    app.register_blueprint(v1.auth, url_prefix="/auth_service/auth/api/v1/")
    app.register_blueprint(v1.user, url_prefix="/auth_service/user/api/v1/")
    app.register_blueprint(v1.media, url_prefix="/profile/media/")
    app.register_blueprint(bp_errors)
    if not config.DEBUG:
        app.register_error_handler(HTTPException, handle_exception)


def configure_db(app: Flask) -> None:
    init_db(app)
    app.app_context().push()


def configure_upload_files(app: Flask) -> None:
    app.config["UPLOAD_FOLDER"] = config.UPLOAD.FOLDER
    app.config["MAX_CONTENT_LENGTH"] = config.UPLOAD.MAX_CONTENT_LENGTH


def configure_ma(app: Flask) -> None:
    init_ma(app)


def configure_jwt(app: Flask) -> None:
    app.config["JWT_SECRET_KEY"] = config.JWT.SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = config.JWT.ACCESS_EXPIRE
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = config.JWT.REFRESH_EXPIRE
    jwt.init_app(app)


def configure_swagger(app: Flask) -> None:
    app.config["SWAGGER"] = {
        "title": "Auth API",
        "uiversion": 3,
        "specs_route": "/swagger/",
        "static_url_path": "/flasgger_static",
        "url_prefix": "/auth_service",
        "specs": [
            {
                "endpoint": "swagger",
                "route": "/swagger/swagger.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
    }
    swagger.init_app(app)


def configure_datastore(app: Flask) -> None:
    security.init_app(app, datastore)


def create_app() -> Flask:
    """Create a Flask app"""

    app = Flask(__name__, instance_relative_config=True)
    app.config["SECRET_KEY"] = config.APP.SECRET_KEY

    configure_db(app)
    configure_upload_files(app)
    configure_ma(app)
    configure_jwt(app)
    configure_logger(app)
    configure_blueprints(app)
    configure_swagger(app)
    configure_datastore(app)
    init_token_check(app)
    admin_grpc_client.client = admin_grpc_client_cls.create()

    return app


app = create_app()

if __name__ == "__main__":
    app = create_app()
    app.run(debug=config.DEBUG, host="0.0.0.0", port=5000)
