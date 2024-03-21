import logging
from pydoc import locate

from celery import Celery

from core.config import get_settings as settings
from grpc_components import notification_grpc_client, admin_grpc_client

notification_grpc_client_cls = locate(settings.NOTIFICATION_GRPC.CLS)
admin_grpc_client_cls = locate(settings.ADMIN_GRPC.CLS)


app = Celery(settings.PROJECT_NAME, broker=settings.CELERY.BROKER_URL, backend=settings.CELERY.BROKER_URL,
             include=['worker.tasks'])
app.conf.update(
    result_expires=3600,
)
app.autodiscover_tasks()


def startup():
    logging.info('startup start')
    notification_grpc_client.client = notification_grpc_client_cls.create_sync()
    admin_grpc_client.client = admin_grpc_client_cls.create_sync()


def shutdown():
    notification_grpc_client.client.close_sync()
    admin_grpc_client.client.close_sync()


if __name__ == '__main__':
    logging.info('%s - Server starts' % settings.PROJECT_NAME)
    try:
        startup()
        app.start(["worker", "-l", "info"])
    except KeyboardInterrupt:
        pass
    finally:
        shutdown()
        logging.info('%s - Server stopped' % settings.PROJECT_NAME)
