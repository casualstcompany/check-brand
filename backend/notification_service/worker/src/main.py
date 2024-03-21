import asyncio
import logging
from pydoc import locate

import db
from components import admin_grpc
from core.config import get_settings as settings
from services.broker_service import get_broker_service as broker_service

_cleanup_coroutines = []
broker_cls = locate(settings.BROKER_MESSAGE.CLS)
admin_grpc_client_cls = locate(settings.ADMIN_GRPC.CLS)


async def startup_before_server_start():
    logging.info("Running functions before starting the server...")
    _cleanup_coroutines.append(server_graceful_shutdown())

    admin_grpc.admin_grpc_client = await admin_grpc_client_cls.create()
    db.msg_broker = await broker_cls.create()


async def server_graceful_shutdown():
    logging.info("Starting graceful shutdown...")
    await db.msg_broker.close()
    await admin_grpc.admin_grpc_client.close()
    await asyncio.sleep(2)


async def main():
    await startup_before_server_start()
    await db.msg_broker.queue_broker.consume(broker_service.process_message)
    await asyncio.Future()


if __name__ == '__main__':
    logging.info(f'{settings.PROJECT_NAME} - Server starts')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(*_cleanup_coroutines)
        loop.close()
        logging.info(f'{settings.PROJECT_NAME} - Server stopped')
