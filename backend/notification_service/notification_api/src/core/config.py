import os
from logging import config as logging_config

from pydantic import BaseSettings

from core.logger import LOGGING


class BrokerMessageSettings:
    CLS: str = 'db.rabbitmq.BrokerDBRabbitMQ'
    HOST: str = os.getenv("BROKER_HOST")
    PORT: int = os.getenv("BROKER_PORT")
    USER: str = os.getenv("BROKER_USER")
    PASSWORD: str = os.getenv("BROKER_PASSWORD")
    DECLARE_EXCHANGE_NAME: str = "topic_notification"


class CacheSettings:
    DRIVER: str = 'redis'
    USER: str = 'user'
    CLS: str = 'db.cache.CacheService'
    HOST: str = os.getenv("CACHE_HOST")
    PORT: int = os.getenv("CACHE_PORT")
    PASSWORD: str = os.getenv("CACHE_PASSWORD")


class GRPCServerSettings:
    PORT: int = int(os.getenv("GRPC_SERVER_PORT"))


class Settings(BaseSettings):
    PROJECT_NAME: str = "NOTIFICATION_API"
    DEBUG = (os.getenv('DEBUG', 'False') == 'True')
    BROKER_MESSAGE: BrokerMessageSettings = BrokerMessageSettings()
    GRPC_SERVER: GRPCServerSettings = GRPCServerSettings()
    CACHE: CacheSettings = CacheSettings()


get_settings = Settings()

if get_settings.DEBUG:
    LOGGING["root"]["level"] = "DEBUG"

logging_config.dictConfig(LOGGING)
