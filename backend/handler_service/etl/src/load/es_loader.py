import json
import logging
from typing import List, Type

import backoff
from elasticsearch import Elasticsearch

from load import BaseLoader
from models import BaseExtractLoadSchema

logger = logging.getLogger(__name__)


class ESLoader(BaseLoader):
    """Class to work with Elasticsearch engine"""

    def __init__(self, host: str, port: str, ca_certs: str, user: str, password: str, bulk_limit: int = 1000):
        super().__init__()
        self.client = Elasticsearch(
            f"https://{host}:{port}",
            ca_certs=ca_certs,
            basic_auth=(user, password)
        )
        self.bulk_limit = bulk_limit

    @backoff.on_exception(backoff.expo, Exception, max_tries=7, jitter=None)
    def create_index(self, model: Type[BaseExtractLoadSchema]) -> None:
        """
        Создание индекса, если он отсутствует
        Если файла со схемой нет, то она сгенерируется автоматически
        из модели при загрузке данных.
        """

        index = model.get_class_meta().table
        file_mapping = model.get_class_meta().file_mapping

        if not self.client.indices.exists(index=index):
            logging.debug('%s - index not exist' % index)

            if file_mapping:
                with open(file_mapping, 'r') as f:
                    mapping = json.load(f)
                    self.client.indices.create(index=index, body=mapping)

    @backoff.on_exception(backoff.expo, Exception, max_tries=7, jitter=None)
    def load_data_bulk(self, model: Type[BaseExtractLoadSchema], data_list: List) -> None:
        """Грузит пачкой в ES, bulk принимает не более 1000 документов за раз"""
        logging.debug('Start load bulk')

        index = model.get_class_meta().table

        while len(data_list) > self.bulk_limit:
            logging.debug('отправляем 1000-1 документов')

            new_lst = data_list[0: self.bulk_limit - 1]
            data_list = data_list[self.bulk_limit - 1:]

            self.client.bulk(body='\n'.join(new_lst) + '\n', index=index)

        self.client.bulk(body='\n'.join(data_list) + '\n', index=index)
        logging.debug('Все документы загружены')
