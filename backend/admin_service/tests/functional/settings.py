from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    db_user = Field("admin", env="DB_USER")
    db_password = Field("password", env="DB_PASSWORD")
    db_host = Field("host.docker.internal", env="DB_HOST")
    db_port = Field(5432, env="DB_PORT")
    db_database_name = Field("base_name", env="DB_NAME")
    db_scheme = "content"

    service_protocol: str = Field("http", env="SERVICE_PROTOCOL")
    service_host: str = Field("host.docker.internal", env="SERVICE_HOST")
    service_port: str = Field("8000", env="SERVICE_PORT")

general_settings = TestSettings()