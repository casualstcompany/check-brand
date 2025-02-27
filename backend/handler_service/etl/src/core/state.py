import abc
import json
import logging
from typing import Optional, Any


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        """Сохранить состояние в постоянное хранилище"""
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        """Загрузить состояние из постоянного хранилища"""
        pass


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path

    def save_state(self, state: dict) -> None:
        if self.file_path is None:
            return

        with open(self.file_path, 'w') as f:
            json.dump(state, f)

    def retrieve_state(self) -> dict:
        if self.file_path is None:
            logging.info('No state file provided. Continue with in-memory state')
            return {}

        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                if not data:
                    return {}

            return data

        except FileNotFoundError:
            self.save_state({})


class State:
    def __init__(self, storage: BaseStorage):
        self.storage = storage
        self.state = self.retrieve_state()

    def retrieve_state(self) -> dict:
        data = self.storage.retrieve_state()
        if not data:
            return {}
        return data

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа"""
        self.state[key] = value

        self.storage.save_state(self.state)

    def get_state(self, key: str, default: Optional[str] = None) -> Any:
        """
            Получить состояние по определённому ключу
            или значение по умолчанию
        """
        data = self.state.get(key)

        if data:
            return data

        return default
