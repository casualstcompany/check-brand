import os
from datetime import datetime, timedelta
from logging import config as logging_config

from pydantic import Field
from pydantic_settings import BaseSettings

from .logger import LOGGING

logging_config.dictConfig(LOGGING)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class AppConfig(BaseSettings):
    SECRET_KEY: str = Field(default="secret-key", env="SECRET_KEY")


class UploadConfig(BaseSettings):
    FOLDER: str = os.path.dirname(BASE_DIR) + "/media"
    MAX_CONTENT_LENGTH: int = 10 * 1000 * 1000


class PostgresConfig(BaseSettings):
    USER: str = "postgres"
    PASSWORD: str = "postgres"
    NAME: str = "database"
    HOST: str = "db"
    PORT: int = 5432

    class Config:
        env_prefix = "DB_"


class RolesAccessConfig(BaseSettings):
    """Указание номеров ролей имеющих доступ к ресурсам определенных видов"""

    # TODO: уточнить у Игоря, Какие роли за кокие ресурсы отвечают
    ACCOUNT: list = [4]
    COLLECTION: list = [5, 6, 7, 8, 10, 11]
    PACK: list = [9]


class ConfigAdminGRPC(BaseSettings):
    CLS: str = "components.admin_grpc_client.AdminGrpcClient"
    HOST: str = "localhost"
    PORT: str = "50053"

    class Config:
        env_prefix = "ADMIN_GRPC_"


class RedisConfig(BaseSettings):
    HOST: str = "redis"
    PASSWORD: str = os.getenv("REDIS_PASSWORD")
    PORT: int = 6379

    class Config:
        env_prefix = "REDIS_"


class JWTConfig(BaseSettings):
    SECRET_KEY: str = "super-secret-jwt-key"
    ACCESS_EXPIRE: timedelta = timedelta(minutes=10)
    REFRESH_EXPIRE: timedelta = timedelta(days=15)

    class Config:
        env_prefix = "JWT_"


class EmailConfig(BaseSettings):
    TEMPLATES: str = os.path.dirname(BASE_DIR) + "/app/template/"
    HOST: str = "smtp.timeweb.ru"
    PORT: int = 465
    HOST_USER: str = "info@checkbrand.com"
    HOST_PASSWORD: str = "111111"
    DEFAULT_FROM_EMAIL: str = "info@checkbrand.com"

    class Config:
        env_prefix = "AUTH_EMAIL_"


class AuthConfig(BaseSettings):
    # Важный параметр, который на проде всегда должен быть False
    LOCAL_MODE_TESTING: bool = (
        os.getenv("LOCAL_MODE_TESTING", "False") == "True"
    )
    MESSAGE: str = "I am signing my one-time nonce:{nonce}"


class Config(BaseSettings):
    DEBUG: bool = True  # TODO:  Временно
    AUTH: AuthConfig = AuthConfig()
    APP: AppConfig = AppConfig()
    POSTGRES: PostgresConfig = PostgresConfig()
    REDIS: RedisConfig = RedisConfig()
    JWT: JWTConfig = JWTConfig()
    BASE_DIR: str = BASE_DIR
    UPLOAD: UploadConfig = UploadConfig()
    ADMIN_GRPC: ConfigAdminGRPC = ConfigAdminGRPC()
    ROLES_ACCESS: RolesAccessConfig = RolesAccessConfig()
    EMAIL: EmailConfig = EmailConfig()


config = Config()
