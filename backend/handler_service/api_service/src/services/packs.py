from functools import lru_cache

from fastapi import Depends

from db import ElasticManager, get_elastic
from elasticsearch import AsyncElasticsearch
from models import Pack
from services.base import DetailView, ListView


class PackService(DetailView, ListView):
    index = Pack.get_class_meta().index
    model = Pack


@lru_cache()
def get_pack_service(elastic: AsyncElasticsearch = Depends(get_elastic),) -> PackService:
    return PackService(ElasticManager(elastic))
