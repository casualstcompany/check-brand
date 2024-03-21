from abc import ABC, abstractmethod
from typing import Type

from models import BaseExtractLoadSchema


class BaseExtractor(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def _get_data(self, query):
        pass

    @abstractmethod
    def extract(self, model: Type[BaseExtractLoadSchema], last_update_at):
        pass
