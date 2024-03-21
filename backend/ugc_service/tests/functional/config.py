from pydantic import BaseSettings

from functional.settings import test_settings as settings

BASE_URL_AUTH = "{protocol}://{host}:{port}".format(
    protocol=settings.AUTH_SERVICE.PROTOCOL,
    host=settings.AUTH_SERVICE.HOST,
    port=settings.AUTH_SERVICE.PORT
)

BASE_URL_UGC = "{protocol}://{host}:{port}".format(
    protocol=settings.UGC_SERVICE.PROTOCOL,
    host=settings.UGC_SERVICE.HOST,
    port=settings.UGC_SERVICE.PORT
)


class UrlsTestConfig:
    BASE_URL_AUTH_V1 = f"{BASE_URL_AUTH}/auth_service/auth/api/v1"
    BASE_URL_UGC_V1 = f"{BASE_URL_UGC}/ugc_service/api/v1"

    LOGIN_V1: str = f"{BASE_URL_AUTH_V1}/web3/login"
    V1_APPLICATION_USER: str = f"{BASE_URL_UGC_V1}/applications/users"


class TestConfig(BaseSettings):
    URLS = UrlsTestConfig()


test_config = TestConfig()
