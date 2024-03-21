from functools import lru_cache

from fastapi import Depends

from db import ElasticManager, get_elastic
from elasticsearch import AsyncElasticsearch
from models import Account
from services.base import DetailView, ListView


class AccountService(DetailView, ListView):
    index = Account.get_class_meta().index
    model = Account


@lru_cache()
def get_account_service(elastic: AsyncElasticsearch = Depends(get_elastic),) -> AccountService:
    return AccountService(ElasticManager(elastic))
