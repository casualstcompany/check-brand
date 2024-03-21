from abc import ABC, abstractmethod
from typing import Type

from models import BaseExtractLoadSchema


class BaseTransformer(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def transform(self, model: Type[BaseExtractLoadSchema], data):
        pass
