import asyncio
from typing import Any

from aio_pika import ExchangeType, connect_robust

from core.config import get_settings as settings
from db import base


async def declare_reject(channel):
    """Создаем обмен и очередь для отмененных сообщений
       с цель в будущем их обрабатывать
       """
    await channel.declare_exchange(
        name=settings.BROKER_MESSAGE.REJECT_DECLARE_EXCHANGE_NAME,
        type=ExchangeType.TOPIC,
        durable=True
    )
    # TODO: наверное эту очередь потом уберем от сюда
    queue = await channel.declare_queue(
        settings.BROKER_MESSAGE.REJECT_QUEUE_NAME,
        durable=True
    )

    await asyncio.gather(*(
        queue.bind(settings.BROKER_MESSAGE.REJECT_DECLARE_EXCHANGE_NAME, routing_key=routing_key)
        for routing_key in settings.BROKER_MESSAGE.ROUTING_KEYS
    ))


class BrokerDBRabbitMQ(base.MessageBrokerDB):
    template_routing_key: str = '{carrier_type}.{transmission_type}.{importance_type}'

    @classmethod
    async def create(cls) -> Any:
        connection = await connect_robust(f"amqp://{settings.BROKER_MESSAGE.USER}:{settings.BROKER_MESSAGE.PASSWORD}"
                                          f"@{settings.BROKER_MESSAGE.HOST}:{settings.BROKER_MESSAGE.PORT}/", timeout=5)
        channel = await connection.channel()

        await channel.set_qos(prefetch_count=settings.BROKER_MESSAGE.PREFETCH_COUNT)

        await declare_reject(channel)

        queue_broker = await channel.declare_queue(
            settings.BROKER_MESSAGE.QUEUE_NAME,
            arguments={"x-dead-letter-exchange": settings.BROKER_MESSAGE.REJECT_DECLARE_EXCHANGE_NAME},
            durable=True
        )

        await asyncio.gather(*(queue_broker.bind(settings.BROKER_MESSAGE.DECLARE_EXCHANGE_NAME, routing_key=routing_key)
                               for routing_key in settings.BROKER_MESSAGE.ROUTING_KEYS))

        return cls(connection=connection, queue_broker=queue_broker)
