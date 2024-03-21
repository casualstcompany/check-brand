import logging

from core.utils.base import get_content_type_by_status_collection_sync
from grpc_components import notification_grpc_client, admin_grpc_client
from celery_main import app


@app.task
def task_send_notify_added_white_list(payload: dict):
    """
    Вынес в эту функцию обращение к admin сервису для получения коллекции
    и определение какое письмо надо отправить.
    """

    # TODO:
    #  если сервисы не доступны перекладывать задачу на потом

    logging.info("Задача отправлена")
    collection_json, collection_error = admin_grpc_client.client.get_collection_sync(
        collection_id=payload["collection_id"]
    )

    if collection_json:
        payload["collection_name"] = collection_json.name
        payload["collection_image_url"] = collection_json.logo
        content_type = "added_white_list"

        if get_content_type_by_status_collection_sync(collection_json.status):
            content_type = get_content_type_by_status_collection_sync(collection_json.status)
        notification_grpc_client.client.notify_email_unicast_default_sync(
            payload_dict=payload,
            content_type=content_type
        )


@app.task
def task_send_notify(payload: dict, content_type: str, get_collection: bool = False):
    """
    Общая задача отправки уведомления пользователю

    Если get_collection==True -> необходимо в payload передавать collection_id (ПОТОМ МОЖНО СДЕЛАТЬ НА ЭТО ПРОВЕРКУ)
    """

    logging.debug("Задача content_type=%s" % content_type)
    if get_collection:
        collection_json, collection_error = admin_grpc_client.client.get_collection_sync(
            collection_id=payload["collection_id"]
        )

        if collection_json:
            payload["collection_name"] = collection_json.name
            payload["collection_image_url"] = collection_json.logo

    notification_grpc_client.client.notify_email_unicast_default_sync(
        payload_dict=payload,
        content_type=content_type
    )
