from abc import ABC, abstractmethod
from typing import List, Type

from models import BaseExtractLoadSchema


class BaseLoader(ABC):
    client = None

    def __init__(self):
        pass

    @abstractmethod
    def load_data_bulk(self, model: Type[BaseExtractLoadSchema], data_list: List):
        pass

    @abstractmethod
    def create_index(self, model):
        pass
