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


class AdminDBSettings:
    USER: str = os.getenv("ADMIN_DB_USER", default="example_user")
    PASSWORD: str = os.getenv("ADMIN_DB_PASSWORD", default="example_password")
    DBNAME: str = os.getenv("ADMIN_DB_NAME", default="example_db")
    HOST: str = os.getenv("ADMIN_DB_HOST", default="localhost")
    PORT: int = int(os.getenv("ADMIN_DB_PORT", default="5432"))
    DSN: str = f"host={HOST} port={PORT} user={USER} password={PASSWORD} dbname={DBNAME}"


class MainSettings(BaseSettings):
    # DEBUG = (os.getenv('DEBUG', 'False') == 'True')
    DEBUG = True  # TODO: временно это поле, потом разблокировать верхнее
    PROJECT_NAME = "ETL ADMIN DB to Elasticsearch"
    PAUSE_BETWEEN_CYCLES_IN_SECONDS = 5
    ADMIN_DB = AdminDBSettings()
    ES_DB = ElasticSettings()


get_settings = MainSettings()

if get_settings.DEBUG:
    LOGGING["root"]["level"] = "DEBUG"

logging_config.dictConfig(LOGGING)
