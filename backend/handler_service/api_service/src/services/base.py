from abc import ABC, abstractmethod
from typing import Type, List

from db import BaseDBManager
from models import BaseSchema
from models.filter import BaseFilterModel


class BaseView(ABC):
    def __init__(self, db_manager: BaseDBManager):
        self.db_manager = db_manager

    @property
    @abstractmethod
    def index(self):
        pass

    @property
    @abstractmethod
    def model(self):
        pass


class ListView(BaseView, ABC):
    async def get_specific_data(
        self, query_model=Type[BaseFilterModel]
    ) -> (List[BaseSchema], int, int):
        """return: List[BaseSchema], total_hits:int, total_pages:int"""
        data, total_hits = await self.db_manager.search_data(
            body=query_model.get_query(), index=self.index
        )
        if total_hits is None:
            total_hits = 0

        total_pages = (
            total_hits + query_model.page_size - 1
        ) // query_model.page_size

        if data is None:
            data = []

        return (
            [self.model.parse_obj(item) for item in data],
            total_hits,
            total_pages,
        )


class DetailView(BaseView, ABC):
    async def get_by_id(self, obj_id: str):
        item = await self.db_manager.get_by_id(self.index, obj_id=obj_id)

        if not item:
            return None

        return self.model.parse_obj(item)
