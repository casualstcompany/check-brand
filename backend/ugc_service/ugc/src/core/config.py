import os
from logging import config as logging_config
from typing import List

from pydantic import BaseSettings

from core.logger import LOGGING


class ConfigAdminService:
    PROTOCOL: str = os.getenv("ADMIN_PROTOCOL")
    HOST: str = os.getenv("ADMIN_HOST")
    PORT: int = os.getenv("ADMIN_PORT")


class ConfigRedis:
    PASSWORD: str = os.getenv("REDIS_PASSWORD")
    HOST: str = os.getenv("REDIS_HOST")
    PORT: int = os.getenv("REDIS_PORT")


class Postgres:
    USERNAME: str = os.getenv("DB_USER")
    PASSWORD: str = os.getenv("DB_PASSWORD")
    HOST: str = os.getenv("DB_HOST")
    PORT: int = os.getenv("DB_PORT")
    DATABASE: str = os.getenv("DB_NAME")


class ConfigUgcGRPC:
    PORT: str = os.getenv("UGC_GRPC_PORT")


class ConfigNotificationGRPC:
    CLS: str = 'grpc_components.notification_grpc_client.NotificationGrpcClient'
    HOST: str = os.getenv("NOTIFICATION_GRPC_HOST")
    PORT: str = os.getenv("NOTIFICATION_GRPC_PORT")


class ConfigAdminGRPC:
    CLS: str = 'grpc_components.admin_grpc_client.AdminGrpcClient'
    HOST: str = os.getenv("ADMIN_GRPC_HOST")
    PORT: str = os.getenv("ADMIN_GRPC_PORT")


class ConfigGRPC:
    HOST: str = os.getenv("AUTH_GRPC_HOST")
    PORT: str = os.getenv("AUTH_GRPC_PORT")


class ConfigCeleryWorker:
    BROKER_URL = f"redis://:{ConfigRedis().PASSWORD}@{ConfigRedis().HOST}:{ConfigRedis().PORT}/0"


class Settings(BaseSettings):
    DEBUG = (os.getenv('DEBUG', 'False') == 'True')
    BASE_URL = "/ugc_service"
    PROJECT_NAME: str = os.getenv("SERVER_NAME", "ugc_service")
    POSTGRES: Postgres = Postgres()
    GRPC: ConfigGRPC = ConfigGRPC()
    AdminService: ConfigAdminService = ConfigAdminService()
    ALLOWED_ROLES_FOR_MODERATOR:  List = ["admin", "superadmin", "moderator"]
    UgcGRPC: ConfigUgcGRPC = ConfigUgcGRPC()
    NOTIFICATION_GRPC: ConfigNotificationGRPC = ConfigNotificationGRPC()
    ADMIN_GRPC: ConfigAdminGRPC = ConfigAdminGRPC()
    CELERY: ConfigCeleryWorker = ConfigCeleryWorker()


get_settings = Settings()

if get_settings.DEBUG:
    LOGGING["root"]["level"] = "DEBUG"

logging_config.dictConfig(LOGGING)
