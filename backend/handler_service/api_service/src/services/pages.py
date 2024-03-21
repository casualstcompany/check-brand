from functools import lru_cache

from fastapi import Depends

from db import ElasticManager, get_elastic
from elasticsearch import AsyncElasticsearch
from models import Page
from services.base import DetailView, ListView


class PageService(DetailView, ListView):
    index = Page.get_class_meta().index
    model = Page


@lru_cache()
def get_page_service(elastic: AsyncElasticsearch = Depends(get_elastic),) -> PageService:
    return PageService(ElasticManager(elastic))
