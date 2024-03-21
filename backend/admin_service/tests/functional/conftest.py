import asyncio
from dataclasses import dataclass
from typing import Optional

import aiohttp
import pytest_asyncio
from multidict import CIMultiDictProxy



@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest_asyncio.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest_asyncio.fixture(scope="session")
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture
def make_get_request(session):
    async def inner(url: str, params: Optional[dict] = None, headers: Optional[dict] = None) -> HTTPResponse:
        params = params or {}
        async with session.get(url, params=params, headers=headers) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


