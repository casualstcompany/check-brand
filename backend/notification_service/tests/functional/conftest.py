import asyncio
import pytest
import grpc

from functional.settings import test_settings
from functional.protobufs.notification_api_pb2_grpc import NotificationStub


@pytest.fixture(scope="session")
def get_notification_client() -> NotificationStub:
    channel = grpc.insecure_channel(f"{test_settings.NotificationAPI.HOST}:{test_settings.NotificationAPI.PORT}")
    client = NotificationStub(channel)
    return client


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()
