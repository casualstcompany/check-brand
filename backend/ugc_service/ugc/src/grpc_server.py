import asyncio
import logging
from concurrent import futures

import grpc

from grpc_components.protobufs import ugc_grpc_pb2_grpc
from services.ugc_grpc import UgcGRPCService
from main import app
from core.config import get_settings as settings

_cleanup_coroutines = []


async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    ugc_grpc_pb2_grpc.add_UgcGRPCServicer_to_server(UgcGRPCService(app), server)
    insecure_port = f'[::]:{settings.UgcGRPC.PORT}'
    # TODO: тут по возможности заменить на работу с сертификатом
    server.add_insecure_port(insecure_port)

    async def startup_before_server_start():
        logging.info("Running functions before starting the server...")

    async def server_graceful_shutdown():
        logging.info("Starting graceful shutdown...")
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
