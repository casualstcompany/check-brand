import os
from logging import config as logging_config

from pydantic import BaseSettings

from core.logger import LOGGING


class ElasticSettings:
    HOST: str = os.getenv("ES_HOST", "localhost")
    PORT: int = os.getenv("ES_PORT", "9200")
    USER: int = os.getenv("ES_USER", "elastic")
    PASSWORD: int = os.getenv("ES_PASSWORD", "Test12345QA")
    PATH_CRT: int = os.getenv("ES_PATH_CA_CRT", "volumes/ca.crt")


class CacheSettings:
    DRIVER: str = 'redis'
    USER: str = 'user'
    CLS: str = 'db.cache.CacheService'
    HOST: str = os.getenv("CACHE_HOST")
    PORT: int = os.getenv("CACHE_PORT")
    PASSWORD: str = os.getenv("CACHE_PASSWORD")


class Settings(BaseSettings):
    # DEBUG = (os.getenv('DEBUG', 'False') == 'True')
    DEBUG = True  # TODO: временно это поле, потом разблокировать верхнее
    BASE_URL = "/handler_service"
    PROJECT_NAME: str = os.getenv("SERVER_NAME", "HandlerServiceApiService")
    ES_DB = ElasticSettings()
    CACHE: CacheSettings = CacheSettings()


get_settings = Settings()

if get_settings.DEBUG:
    LOGGING["root"]["level"] = "DEBUG"

logging_config.dictConfig(LOGGING)
