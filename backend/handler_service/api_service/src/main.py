from pydoc import locate

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from elasticsearch import AsyncElasticsearch

from api import v1 as api_v1

from db import elastic
from db import cache
from core.config import get_settings as settings

cache_cls = locate(settings.CACHE.CLS)

app = FastAPI(
    title="FAST SERVICE API",
    version="1.0.0",
    description="Сервис для быстрой фильтрации и выводы запрошенной информации",
    docs_url=settings.BASE_URL + "/swagger",
    openapi_url=settings.BASE_URL + "/openapi.json",
    default_response_class=ORJSONResponse,
    redoc_url=None,
    debug=settings.DEBUG
)


@app.on_event('startup')
async def startup():
    elastic.es = AsyncElasticsearch(
        f"https://{settings.ES_DB.HOST}:{settings.ES_DB.PORT}",
        ca_certs=settings.ES_DB.PATH_CRT,
        basic_auth=(settings.ES_DB.USER, settings.ES_DB.PASSWORD)
    )
    cache.cache = await cache_cls.create()


@app.on_event('shutdown')
async def shutdown():
    await elastic.es.close()
    await cache.cache.close()


app.include_router(api_v1.router, prefix=settings.BASE_URL + '/api/v1')


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7000, reload=True)
