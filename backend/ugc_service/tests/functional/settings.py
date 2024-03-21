import os
from typing import List

from pydantic import BaseSettings


class AUTHDBSettings:
    USER: str = os.getenv("AUTH_DB_USER", default="admin")
    PASSWORD: str = os.getenv("AUTH_DB_PASSWORD", default="password")
    DBNAME: str = os.getenv("AUTH_DB_NAME", default="auth_database")
    HOST: str = os.getenv("AUTH_DB_HOST", default="localhost")
    PORT: int = int(os.getenv("AUTH_DB_PORT", default="5431"))
    DSN: str = f"host={HOST} port={PORT} user={USER} password={PASSWORD} dbname={DBNAME}"
    DROP_SCHEMA: str = "content"
    PATH_LOAD_DATA: str = "./testdata/db/auth/auth_dump.sql"


class AdminDBSettings:
    USER: str = os.getenv("ADMIN_DB_USER", default="admin")
    PASSWORD: str = os.getenv("ADMIN_DB_PASSWORD", default="password")
    DBNAME: str = os.getenv("ADMIN_DB_NAME", default="auth_database")
    HOST: str = os.getenv("ADMIN_DB_HOST", default="localhost")
    PORT: int = int(os.getenv("ADMIN_DB_PORT", default="5431"))
    DSN: str = f"host={HOST} port={PORT} user={USER} password={PASSWORD} dbname={DBNAME}"
    DROP_SCHEMA: str = "content"
    PATH_LOAD_DATA: List[str] = ["./testdata/db/admin/admin_dump.sql", "./testdata/db/admin/token.sql"]


class UGCServiceSettings:
    PROTOCOL = os.getenv("UGC_PROTOCOL", default="http")
    HOST = os.getenv("UGC_HOST", default="localhost")
    PORT = os.getenv("UGC_PORT", default="6000")


class UGCServiceGRPCSettings:
    HOST = os.getenv("UGC_GRPC_HOST", default="localhost")
    PORT = os.getenv("UGC_GRPC_PORT", default="50056")


class AUTHServiceSettings:
    PROTOCOL = os.getenv("AUTH_PROTOCOL", default="http")
    HOST = os.getenv("AUTH_HOST", default="localhost")
    PORT = os.getenv("AUTH_PORT", default="6000")


class AUTHServiceGRPCSettings:
    HOST = os.getenv("AUTH_GRPC_HOST", default="localhost")
    PORT = os.getenv("AUTH_GRPC_PORT", default="50056")


class TestSettings(BaseSettings):
    UGC_SERVICE = UGCServiceSettings()
    UGC_GRPC_SERVICE = UGCServiceGRPCSettings()
    AUTH_DB = AUTHDBSettings()
    ADMIN_DB = AdminDBSettings()
    AUTH_SERVICE = AUTHServiceSettings()
    AUTH_GRPC_SERVICE = AUTHServiceGRPCSettings()


test_settings = TestSettings()
