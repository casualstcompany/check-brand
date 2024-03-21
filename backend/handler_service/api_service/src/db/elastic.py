import logging
from typing import Optional, List

import backoff
from elasticsearch import AsyncElasticsearch, ConnectionError, NotFoundError

from .base import BaseDBManager

es: Optional[AsyncElasticsearch] = None


class ElasticManager(BaseDBManager):
    def __init__(self, elasticsearch: AsyncElasticsearch):
        self.elasticsearch = elasticsearch

    @backoff.on_exception(backoff.expo, ConnectionError, max_time=10, factor=2)
    async def get_by_id(self, index: str, obj_id: str):
        try:
            doc = await self.elasticsearch.get(index=index, id=obj_id)
        except NotFoundError:
            return None
        if doc["_source"]["hide"]:
            return None
        return doc["_source"]

    @backoff.on_exception(backoff.expo, ConnectionError, max_time=10, factor=2)
    async def search_data(self, index, body=None) -> (List[dict], int):
        """return: List[dict], total_hits:int"""
        try:
            data = await self.elasticsearch.search(body=body, index=index)

        except Exception as e:
            # TODO: тут только возможные ошибки отлавливать
            logging.error(e)
            return None, None

        return [item["_source"] for item in data["hits"]["hits"]], data[
            "hits"
        ]["total"]["value"]


async def get_elastic() -> AsyncElasticsearch:
    return es
