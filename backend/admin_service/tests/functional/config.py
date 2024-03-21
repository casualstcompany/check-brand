from functional.settings import general_settings as settings
from sqlalchemy import MetaData, create_engine
from pydantic import BaseSettings


BASE = "{protocol}://{host}:{port}".format(protocol=settings.service_protocol,
                                           host=settings.service_host,
                                           port=settings.service_port)

ADMIN_PANEL_URL_V1 = f"{BASE}/admin_service/api/v1"


# noinspection SyntaxError
class TestUrls:
    page: str = ADMIN_PANEL_URL_V1 + "/page/"
    account: str = ADMIN_PANEL_URL_V1 + "/account/"
    collection: str = ADMIN_PANEL_URL_V1 + "/collection/"
    pack: str = ADMIN_PANEL_URL_V1 + "/pack/"
    token: str = ADMIN_PANEL_URL_V1 + "/token/"


class DatabaseConfig:
    ENGINE = create_engine("postgresql://{user}:{password}@{host}:{port}/{database_name}".format(
        user=settings.db_user,
        password=settings.db_password,
        host=settings.db_host,
        port=settings.db_port,
        database_name=settings.db_database_name,
    ))
    TRACK_MODIFICATIONS = False
    SCHEMA = settings.db_scheme
    metadata = MetaData(schema=settings.db_scheme)


class Config(BaseSettings):
    DatabaseConfig = DatabaseConfig()


config = Config()
