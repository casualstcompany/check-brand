import os
from logging import config as logging_config

from pydantic import BaseSettings

from core.logger import LOGGING


class AdminGRPCSettings:
    CLS: str = 'components.admin_grpc.AdminGrpcClient'
    HOST: str = os.getenv("ADMIN_GRPC_HOST")
    PORT: int = os.getenv("ADMIN_GRPC_PORT")


class EmailDeliveryServiceSettings:
    DOMAIN_NAME: str = os.getenv("EMAIL_DELIVERY_DOMAIN_NAME")
    API_KEY: str = os.getenv("EMAIL_DELIVERY_API_KEY")
    BASE_URL: int = os.getenv("EMAIL_DELIVERY_BASE_URL")
    DEFAULT_FROM_EMAIL: str = os.getenv("EMAIL_DELIVERY_DEFAULT_FROM_EMAIL")
    NAME_SENDER: str = os.getenv("EMAIL_DELIVERY_NAME_SENDER")


class BrokerMessageSettings:
    CLS: str = 'db.rabbitmq.BrokerDBRabbitMQ'
    HOST: str = os.getenv("BROKER_HOST")
    PORT: int = os.getenv("BROKER_PORT")
    USER: str = os.getenv("BROKER_USER")
    PASSWORD: str = os.getenv("BROKER_PASSWORD")
    DECLARE_EXCHANGE_NAME: str = "topic_notification"

    ROUTING_KEYS: list[str] = [
        'EMAIL.UNICAST.HIGH', 'EMAIL.UNICAST.DEFAULT', 'EMAIL.UNICAST.LOW',
        'EMAIL.MULTICAST.HIGH', 'EMAIL.MULTICAST.DEFAULT', 'EMAIL.MULTICAST.LOW'
    ]
    QUEUE_NAME: str = 'email_unicast'
    REJECT_DECLARE_EXCHANGE_NAME: str = "reject_topic_notification"
    REJECT_QUEUE_NAME: str = 'reject_email_unicast'
    PREFETCH_COUNT: int = int(os.getenv("BROKER_PREFETCH_COUNT"))
    TIME_SLEEP: int = int(os.getenv("BROKER_TIME_SLEEP"))


class Settings(BaseSettings):
    PROJECT_NAME: str = "NOTIFICATION_WORKER"
    DEBUG = (os.getenv('DEBUG', 'False') == 'True')
    BROKER_MESSAGE: BrokerMessageSettings = BrokerMessageSettings()
    ADMIN_GRPC: AdminGRPCSettings = AdminGRPCSettings()
    EMAIL_DELIVERY: EmailDeliveryServiceSettings = EmailDeliveryServiceSettings()


get_settings = Settings()

if get_settings.DEBUG:
    LOGGING["root"]["level"] = "DEBUG"

logging_config.dictConfig(LOGGING)
