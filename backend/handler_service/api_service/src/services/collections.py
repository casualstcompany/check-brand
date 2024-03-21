from functools import lru_cache

from fastapi import Depends

from db import ElasticManager, get_elastic
from elasticsearch import AsyncElasticsearch
from models import Collection
from services.base import DetailView, ListView


class CollectionService(DetailView, ListView):
    index = Collection.get_class_meta().index
    model = Collection


@lru_cache()
def get_collection_service(elastic: AsyncElasticsearch = Depends(get_elastic),) -> CollectionService:
    return CollectionService(ElasticManager(elastic))
