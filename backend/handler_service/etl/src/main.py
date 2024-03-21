import logging
from datetime import datetime
from time import sleep
from typing import List, Type

from core.config import get_settings as settings
from core.state import JsonFileStorage, State
from extract import BaseExtractor, PostgresExtractor
from load import BaseLoader, ESLoader
from models import BaseExtractLoadSchema, TokenExtractLoad, PackExtractLoad, \
    CollectionExtractLoad, AccountExtractLoad, PageExtractLoad
from transform import BaseTransformer, ESTransformer


class ETLProcess:
    def __init__(self, state: State,
                 extractor: BaseExtractor, transformer: BaseTransformer,  loader: BaseLoader,
                 list_models: List[Type[BaseExtractLoadSchema]]):

        self.state = state
        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader
        self.list_models = list_models

    def run(self):
        """Соединяет воедино три кита и запускает их)))"""

        """
        При первом старте будут создавться индексы отдельно, 
        так как через mapping можно настроить более подробную 
        структуру хранения и индексирования
        """
        for model in self.list_models:
            self.loader.create_index(model=model)

        while True:
            for model in self.list_models:

                last_update_at = self.state.get_state(
                    model.get_class_meta().state_key_update_at, default=str(datetime.min)
                )

                logging.debug("%s - %s" % (model.get_class_meta().state_key_update_at, last_update_at))

                results = self.extractor.extract(model=model, last_update_at=last_update_at)

                if results:
                    logging.debug("new result")

                    new_last_update_at = results[-1][-1]
                    results = self.transformer.transform(model=model, data=results)

                    self.loader.load_data_bulk(model=model, data_list=results)

                    self.state.set_state(model.get_class_meta().state_key_update_at, str(new_last_update_at))

            logging.debug("Pause %s seconds" % str(settings.PAUSE_BETWEEN_CYCLES_IN_SECONDS))

            sleep(settings.PAUSE_BETWEEN_CYCLES_IN_SECONDS)


def create_etl_process():
    """Подготавливаем процесс ETL"""

    state = State(JsonFileStorage('volumes/etl_state.json'))

    extractor = PostgresExtractor(dsn=settings.ADMIN_DB.DSN)
    transformer = ESTransformer()
    loader = ESLoader(
        host=settings.ES_DB.HOST,
        port=str(settings.ES_DB.PORT),
        ca_certs=settings.ES_DB.PATH_CRT,
        user=settings.ES_DB.USER,
        password=settings.ES_DB.PASSWORD,
    )

    list_models = [
        TokenExtractLoad,
        PackExtractLoad,
        CollectionExtractLoad,
        AccountExtractLoad,
        PageExtractLoad,
    ]

    return ETLProcess(
        state=state,
        extractor=extractor,
        transformer=transformer,
        loader=loader,
        list_models=list_models
    )


if __name__ == "__main__":
    etl = create_etl_process()
    try:
        logging.info('%s - Starts' % settings.PROJECT_NAME)
        etl.run()
    except KeyboardInterrupt:
        pass
    finally:
        logging.info('%s - Finish' % settings.PROJECT_NAME)
