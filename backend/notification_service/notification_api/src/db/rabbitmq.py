import logging
from typing import Any

from aio_pika import DeliveryMode, ExchangeType, Message, connect

from core.config import get_settings as settings
from db import base
from models.messages import QueueMessage


class BrokerDBRabbitMQ(base.MessageBrokerDB):
    template_routing_key: str = '{carrier_type}.{transmission_type}.{importance_type}'

    @classmethod
    async def create(cls) -> Any:
        connection = await connect(f"amqp://{settings.BROKER_MESSAGE.USER}:{settings.BROKER_MESSAGE.PASSWORD}"
                                   f"@{settings.BROKER_MESSAGE.HOST}:{settings.BROKER_MESSAGE.PORT}/", timeout=5)
        channel = await connection.channel()

        topic_declare_exchange = await channel.declare_exchange(
            name=settings.BROKER_MESSAGE.DECLARE_EXCHANGE_NAME,
            type=ExchangeType.TOPIC,
            durable=True
        )
        return cls(connection=connection, topic_declare_exchange=topic_declare_exchange)

    async def put(self, message: QueueMessage, carrier_type: str, transmission_type: str, importance_type: str) -> None:
        logging.debug("put message")
        routing_key = self.template_routing_key.format(
            carrier_type=carrier_type,
            transmission_type=transmission_type,
            importance_type=importance_type
        )

        await self.topic_declare_exchange.publish(
            Message(body=message.json().encode('utf-8'), delivery_mode=DeliveryMode.PERSISTENT),
            routing_key=routing_key
        )
