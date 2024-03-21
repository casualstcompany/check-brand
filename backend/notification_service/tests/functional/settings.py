import os

from pydantic import BaseSettings


class NotificationAPI:
    HOST = os.getenv("NOTIFICATION_API_HOST", default="localhost")
    PORT = os.getenv("NOTIFICATION_API_PORT", default="50053")


class TestSettings(BaseSettings):
    NotificationAPI = NotificationAPI()


test_settings = TestSettings()
