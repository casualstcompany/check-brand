import logging
from contextlib import closing
from typing import Type

import backoff
import psycopg2
from psycopg2 import sql

from core.query import BASE_TEMPLATE_EXTRACT_QUERY_SQL
from extract.base_extractor import BaseExtractor
from models import BaseExtractLoadSchema


class PostgresExtractor(BaseExtractor):

    def __init__(self, dsn):
        super().__init__()
        self.dsn = dsn

    @backoff.on_exception(backoff.expo, Exception, max_tries=7, jitter=None)
    def _get_data(self, query):
        with self.conn.cursor() as curs:
            curs.execute(query)
            results = curs.fetchall()
            return results

    @staticmethod
    def _get_sql_query(model: Type[BaseExtractLoadSchema], last_update_at):
        """ Формируем запрос на основе базового шаблона """
        model_meta = model.get_class_meta()

        complex_fields_comma = sql.SQL('')
        if model.get_names_complex_fields():
            complex_fields_comma = sql.SQL(' ,')

        query = BASE_TEMPLATE_EXTRACT_QUERY_SQL.format(
            model_list_simple_field_names=sql.SQL(',').join(sql.SQL(n) for n in model.get_list_names_simple_fields()),
            model_list_complex_fields_meta_array_agg=sql.SQL(',').join(
                sql.SQL(n) for n in model.get_list_complex_fields_meta_array_agg()) + complex_fields_comma,
            model_list_complex_fields_meta_left_join=sql.SQL(' ').join(
                sql.SQL(n) for n in model.get_list_complex_fields_meta_left_join()),
            model_meta_schema=sql.Identifier(model_meta.schema),
            model_meta_table=sql.Identifier(model_meta.table),
            model_meta_greatest=sql.SQL(model.get_greatest()),
            model_meta_greatest_no_max=sql.SQL(model.get_greatest(not_max=True)),
            model_meta_field_group_by=sql.Identifier(model_meta.field_group_by),
            last_update_at=sql.SQL(last_update_at),
        )
        return query

    @backoff.on_exception(backoff.expo, Exception, max_tries=7, jitter=None)
    def extract(self, model: Type[BaseExtractLoadSchema], last_update_at):
        """ Извлечение данных из Postgres по определенной модели и дате обновления"""

        with closing(psycopg2.connect(dsn=self.dsn)) as self.conn:
            logging.debug('Postgres connection is open. Start load data')

            query = self._get_sql_query(model=model, last_update_at=last_update_at)
            data = self._get_data(query=query)

            if not data:
                logging.info('No updates')

            return data
