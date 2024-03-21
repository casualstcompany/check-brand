from functools import lru_cache

from fastapi import Depends

from db import ElasticManager, get_elastic
from elasticsearch import AsyncElasticsearch
from models import Token
from services.base import DetailView, ListView


class TokenService(DetailView, ListView):
    index = Token.get_class_meta().index
    model = Token


@lru_cache()
def get_token_service(elastic: AsyncElasticsearch = Depends(get_elastic),) -> TokenService:
    return TokenService(ElasticManager(elastic))
