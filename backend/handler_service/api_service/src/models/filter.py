from datetime import datetime
from typing import Optional, List
from uuid import UUID

from fastapi import Query
from pydantic import Field

from models.base import BaseSchema
from models.enum import (
    StatusPriceTypeEnum,
    StatusTypeEnum,
    SortByTokenEnum,
    SortByCollectionRankingsEnum,
    SortByPackEnum,
    SortByCollectionEnum,
    SortByAccountEnum,
    SortByPageEnum,
)


class BaseFilterModel(BaseSchema):
    """Модель предназначена для:
    - Указания параметров фильтрации, сортировки и поиска данных.
    - Преобразования полученных значений в узнаваемый запрос к elasticsearch.
    """

    q: Optional[str] = Query(None, title="Поиск")
    sort_by: Optional[List[str]] = Field(
        Query(None, title="Сортировка по полям")
    )
    page: Optional[int] = Query(1, title="Номер страницы", gt=0)
    page_size: Optional[int] = Query(10, title="Размер страницы", gt=0)

    class Config:
        reserved_fields = ["q", "sort_by", "page", "page_size"]

    class Meta:
        range_fields = []
        search_fields = ["name", "description"]
        special_fields = {"collection_id": "collection.id"}

    def get_filter(self):
        """Собирает и возвращает список для фильтрации
        Пример: [{'terms': {'status': ['book']}}]
        """
        filters = [{"term": {"hide": False}}]

        for field_name in self.__fields__.keys():

            if field_name in self.Meta.range_fields:
                value = getattr(self, field_name)
                if value and len(field_name.split("__")) == 2:
                    filters.append(
                        {
                            "range": {
                                field_name.split("__")[0]: {
                                    field_name.split("__")[1]: value
                                }
                            }
                        }
                    )

            elif field_name not in self.Config.reserved_fields:
                value = getattr(self, field_name)

                if self.Meta.special_fields.get(field_name):
                    """Необходимо, если поле является объектом, а мы фильтруем например по его id"""
                    field_name = self.Meta.special_fields.get(field_name)

                if value:
                    if isinstance(value, list):
                        filters.append({"terms": {field_name: value}})
                    else:
                        filters.append({"term": {field_name: value}})

        return filters

    def get_search(self):
        """Возвращает словарь необходимый
        для поиска среди указанных полей в self.Meta.search_fields
        по полученному значению."""
        value = getattr(self, "q")

        if value:
            return {
                "multi_match": {
                    "query": value,
                    "fuzziness": "auto",
                    "fields": self.Meta.search_fields,
                }
            }

        return None

    def get_from_index(self):
        """Возвращает порядковый номер объекта из всего списка,
        который будет первым на указанной странице."""
        return (self.page - 1) * self.page_size

    def get_sort(self):
        """Собирает и возвращает список для сортировки
        Пример: [{'price': {'order': 'desc'}}]
        """
        values = getattr(self, "sort_by")

        if values:
            sort = []

            for field in values:
                sort.append(
                    {
                        field.lstrip("-"): {
                            "order": (
                                "asc" if not field.startswith("-") else "desc"
                            )
                        }
                    }
                )
            return sort

        return None

    def get_query(self):
        """Собирает и возвращает весь query для elasticsearch"""
        query = {"query": {"bool": {}}}

        filters = self.get_filter()

        if filters:
            query["query"]["bool"]["filter"] = filters

        search = self.get_search()

        if search:
            query["query"]["bool"]["must"] = search

        query["from"] = self.get_from_index()
        query["size"] = self.page_size

        sort = self.get_sort()

        if sort:
            query["sort"] = sort

        return query


class TokenFilter(BaseFilterModel):
    sort_by: Optional[List[SortByTokenEnum]] = Field(
        Query(None, title="Сортировка по полям")
    )

    price__gte: Optional[float] = Query(None, title="Цена от - до")
    price__lte: Optional[float] = Query(None, title="Цена от - до")
    status_price: Optional[List[StatusPriceTypeEnum]] = Field(
        Query(None, title="Статус цены")
    )
    status: Optional[List[StatusTypeEnum]] = Field(Query(None, title="Статус"))

    collection_id: Optional[List[UUID]] = Field(
        Query(None, title="ID коллекции")
    )
    pack_id: Optional[List[UUID]] = Field(Query(None, title="ID пакетов"))
    properties_id: Optional[List[UUID]] = Field(
        Query(None, title="ID properties")
    )
    levels_stats_id: Optional[List[UUID]] = Field(
        Query(None, title="ID levels_stats")
    )
    currency_token_id: Optional[List[UUID]] = Field(
        Query(None, title="ID currency_token")
    )

    wallet_owner: Optional[str] = Query(None, title="wallet_owner")
    mint: Optional[bool] = Query(None, title="mint")
    paid: Optional[bool] = Query(None, title="paid")

    class Meta:
        range_fields = ["price__gte", "price__lte"]
        search_fields = ["name", "description"]
        special_fields = {
            "collection_id": "collection.id",
            "pack_id": "pack.id",
            "levels_stats_id": "levels_stats.id",
            "properties_id": "properties.id",
            "currency_token_id": "currency_token.id",
        }


class PackFilter(BaseFilterModel):
    sort_by: Optional[List[SortByPackEnum]] = Field(
        Query(None, title="Сортировка по полям")
    )

    price__gte: Optional[float] = Query(None, title="Цена от - до")
    price__lte: Optional[float] = Query(None, title="Цена от - до")
    status_price: Optional[List[StatusPriceTypeEnum]] = Field(
        Query(None, title="Статус цены")
    )
    status: Optional[List[StatusTypeEnum]] = Field(Query(None, title="Статус"))

    collection_id: Optional[List[UUID]] = Field(
        Query(None, title="ID коллекции")
    )
    properties_id: Optional[List[UUID]] = Field(
        Query(None, title="ID properties")
    )
    levels_stats_id: Optional[List[UUID]] = Field(
        Query(None, title="ID levels_stats")
    )
    currency_token_id: Optional[List[UUID]] = Field(
        Query(None, title="ID currency_token")
    )

    wallet_owner: Optional[str] = Query(None, title="wallet_owner")

    class Meta:
        range_fields = ["price__gte", "price__lte"]
        search_fields = ["name", "description"]
        special_fields = {
            "collection_id": "collection.id",
            "levels_stats_id": "levels_stats.id",
            "properties_id": "properties.id",
            "currency_token_id": "currency_token.id",
        }


class CollectionFilter(BaseFilterModel):
    sort_by: Optional[List[SortByCollectionEnum]] = Field(
        Query(None, title="Сортировка по полям")
    )

    status: Optional[List[StatusTypeEnum]] = Field(Query(None, title="Статус"))

    account_id: Optional[List[UUID]] = Field(Query(None, title="ID account"))
    page_id: Optional[List[UUID]] = Field(Query(None, title="ID page"))
    payment_tokens_id: Optional[List[UUID]] = Field(
        Query(None, title="ID payment tokens")
    )

    class Meta:
        range_fields = []
        search_fields = ["name", "description"]
        special_fields = {
            "account_id": "account.id",
            "page_id": "page.id",
            "payment_tokens_id": "payment_tokens.id",
        }


class CollectionRankingsFilter(BaseFilterModel):
    updated_at__gte: Optional[datetime] = Query(
        None, title="Дата обновления - больше или равно"
    )
    updated_at__lte: Optional[datetime] = Query(
        None, title="Дата обновления - меньше или равно"
    )
    sort_by: Optional[List[SortByCollectionRankingsEnum]] = Field(
        Query(None, title="Сортировка по полям")
    )

    blockchain_id: Optional[List[UUID]] = Field(
        Query(None, title="ID blockchain")
    )
    page_id: Optional[List[UUID]] = Field(Query(None, title="ID page"))

    class Meta:
        range_fields = ["updated_at__gte", "updated_at__lte"]
        search_fields = ["name", "description"]
        special_fields = {
            "blockchain_id": "blockchain.id",
            "page_id": "page.id",
        }


class AccountFilter(BaseFilterModel):
    sort_by: Optional[List[SortByAccountEnum]] = Field(
        Query(None, title="Сортировка по полям")
    )

    page_id: Optional[List[UUID]] = Field(Query(None, title="ID page"))

    class Meta:
        range_fields = []
        search_fields = ["name", "description"]
        special_fields = {
            "page_id": "page.id",
        }


class PageFilter(BaseFilterModel):
    sort_by: Optional[List[SortByPageEnum]] = Field(
        Query(None, title="Сортировка по полям")
    )

    class Meta:
        range_fields = []
        special_fields = {}
        search_fields = ["name", "description", "title_1", "title_2"]
