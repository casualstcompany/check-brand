import asyncio
from typing import Optional
from dataclasses import dataclass

import pytest
import aiohttp
import pytest_asyncio
from multidict import CIMultiDictProxy

from functional.manager.db_manager import ContextManagerDB
from functional.config import test_config as config
from functional.settings import test_settings as settings
from functional.testdata import auth


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest_asyncio.fixture(scope="session")
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def auth_db():
    db = ContextManagerDB(dsn=settings.AUTH_DB.DSN)
    db.drop_schema_cascade(schema_name=settings.AUTH_DB.DROP_SCHEMA)
    db.create_all_by_file(filename=settings.AUTH_DB.PATH_LOAD_DATA)
    yield
    # db.drop_schema_cascade(schema_name=settings.AUTH_DB.DROP_SCHEMA)


@pytest.fixture(scope="session")
def admin_db():
    db = ContextManagerDB(dsn=settings.ADMIN_DB.DSN)
    # TODO: временно остановил разработку тестов, ещё вернусь
    db.drop_schema_cascade(schema_name=settings.ADMIN_DB.DROP_SCHEMA)
    for filename in settings.ADMIN_DB.PATH_LOAD_DATA:
        db.create_all_by_file(filename=filename)
    yield
    # db.drop_schema_cascade(schema_name=settings.ADMIN_DB.DROP_SCHEMA)


@pytest.fixture()
def make_get_request(session):
    async def inner(url: str, params: Optional[dict] = None, headers: Optional[dict] = None) -> HTTPResponse:
        params = params or {}
        async with await session.get(url, params=params, headers=headers) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture()
def make_post_request(session):
    async def inner(url: str, data: dict = None, headers: Optional[dict] = None) -> HTTPResponse:
        async with session.post(url, json=data, headers=headers) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture()
def make_put_request(session):
    async def inner(url: str, data: dict = None, headers: Optional[dict] = None) -> HTTPResponse:
        async with session.put(url, json=data, headers=headers) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture()
async def get_access(admin_db, auth_db, make_post_request):
    response = await make_post_request(
        config.URLS.LOGIN_V1, data=auth.login_data
    )

    return response.body["access_token"]
