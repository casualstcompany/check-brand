import asyncio
import logging
from concurrent import futures
from pydoc import locate

import grpc
from components.grpc.protobufs.notification_api_pb2_grpc import \
    add_NotificationServicer_to_server

import db
from core import config
from core.config import get_settings as settings
from service.notification_service import NotificationServicer

_cleanup_coroutines = []
broker_cls = locate(settings.BROKER_MESSAGE.CLS)
cache_cls = locate(settings.CACHE.CLS)


async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    add_NotificationServicer_to_server(NotificationServicer(), server)
    insecure_port = f'[::]:{config.get_settings.GRPC_SERVER.PORT}'
    server.add_insecure_port(insecure_port)

    async def startup_before_server_start():
        logging.info("Running functions before starting the server...")
        db.msg_broker = await broker_cls.create()
        db.cache = await cache_cls.create()

    async def server_graceful_shutdown():
        logging.info("Starting graceful shutdown...")
        await db.msg_broker.close()
        await db.cache.close()
        await server.stop(5)

    await startup_before_server_start()

    logging.info('Server starts on port %s' % insecure_port)
    await server.start()

    _cleanup_coroutines.append(server_graceful_shutdown())
    await server.wait_for_termination()


if __name__ == '__main__':
    logging.info('%s - Server starts' % settings.PROJECT_NAME)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(serve())
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(*_cleanup_coroutines)
        loop.close()
        logging.info('%s - Server stopped' % settings.PROJECT_NAME)
