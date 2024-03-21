import logging

from celery import shared_task

from nft_tokens.models import Collection, Pack, StatusToken, Token
from nft_tokens.services import (
    account_service_cls,
    collection_service_cls,
    pack_service_cls,
    token_service_cls,
)


@shared_task(bind=True, max_retries=5, retry_backoff=40)
def task_status_update_in_collection(self, collection_id, update_parts=None):
    """
    Параметр "update_parts" отвечает за то, какие части задачи необходимо выполнить, включает:
        "packs_tokens" - Обновляет статусы в pack и token принадлежащих данной коллекции,
        "notification" - Отправляет сигнал для оповещения пользователей,
        "applications" - Обновляет статусы заявок в UGC service.
    """
    logging.debug("Start task_update_status_in_application")

    if update_parts is None:
        update_parts = ["packs_tokens", "applications", "notification"]

    try:
        collection_model = Collection.objects.filter(id=collection_id).first()
        """
            м/б потом уберу
            Т.К до этого все завязывалось на статусах токенов, много чего наверное зависит от них.
            Сейчас все завязываем на статусах Коллекций.
            Как только уберем поля status из токенов и все зависимости к нему,
            отпадет и необходимость обновлять статусы в двух моделях ниже.
        """
        if "packs_tokens" in update_parts:
            Pack.objects.filter(collection=collection_model).update(
                status=collection_model.status
            )
            Token.objects.filter(collection=collection_model).update(
                status=collection_model.status
            )

        # TODO: в дальнейшем убрать дублирование,
        #  сделал так, потому что при sold_out надо в первую очередь выполнить,
        #  надо вынести в отдельную функцию, а может и забить)))
        if "notification" in update_parts:
            if collection_model.status in [StatusToken.sold_out]:
                send_notification = collection_service_cls.send_notification_users_with_white_list(
                    collection_id=collection_id,
                    collection_logo=collection_model.logo.url,
                    collection_name=collection_model.name,
                    status_token=collection_model.status,
                )
                if not send_notification:
                    update_parts = ["applications", "notification"]
                    raise Exception()

        if "applications" in update_parts:
            if collection_model.status in [
                StatusToken.mint_2,
                StatusToken.stop,
                StatusToken.sold_out,
            ]:
                update_applications = (
                    collection_service_cls.send_update_status_in_applications(
                        collection_model.status, collection_id
                    )
                )
                if not update_applications:
                    update_parts = ["applications", "notification"]
                    raise Exception()

        if "notification" in update_parts:
            if collection_model.status in [
                StatusToken.book,
                StatusToken.mint_1,
                StatusToken.mint_2,
            ]:
                send_notification = collection_service_cls.send_notification_users_with_white_list(
                    collection_id=collection_id,
                    collection_logo=collection_model.logo.url,
                    collection_name=collection_model.name,
                    status_token=collection_model.status,
                )
                if not send_notification:
                    update_parts = ["notification"]
                    raise Exception()

    except Exception as e:
        self.retry(args=[collection_id, update_parts], exc=e)

    logging.debug("Finish task_update_status_in_application")


@shared_task(bind=True, max_retries=5, retry_backoff=40)
def task_update_tokens_pack_collection_account(self, pack_id, status):
    logging.debug("Task start: %s" % status)

    try:
        if status == "pack_updated":
            logging.debug("update tokens")
            pack = token_service_cls.get_model_pack(pack_id=pack_id)

            token_service_cls.update_by_pack(pack=pack)

        logging.debug("update pack")
        pack_service_cls.update_counted_fields(model_id=pack_id)

        logging.debug("update collection")
        collection_model = Collection.objects.filter(pack__id=pack_id).first()
        if collection_model:
            collection_service_cls.update_counted_fields(
                model_id=collection_model.id
            )

            logging.debug("update account")
            account_service_cls.update_counted_fields(
                model_id=collection_model.account.id
            )

    except Exception as e:
        self.retry(args=[pack_id, status], exc=e)

    logging.debug("Task finish: %s" % status)


@shared_task(bind=True, max_retries=5, retry_backoff=40)
def task_update_collection_account(self, collection_id, status):
    logging.debug("Task start: %s" % status)

    try:
        logging.debug("update collection")
        collection_model = Collection.objects.filter(id=collection_id).first()
        if collection_model:
            collection_service_cls.update_counted_fields(
                model_id=collection_id
            )

            logging.debug("update account")
            account_service_cls.update_counted_fields(
                model_id=collection_model.account.id
            )
    except Exception as e:
        self.retry(args=[collection_id, status], exc=e)

    logging.debug("Task finish: %s" % status)


@shared_task(bind=True, max_retries=5, retry_backoff=40)
def task_update_account(self, account_id, status):
    logging.debug("Task start: %s" % status)

    try:
        list_params = ["collections_count"]
        account_service_cls.update_counted_fields(
            model_id=account_id, list_params=list_params
        )

    except Exception as e:
        self.retry(args=[account_id, status], exc=e)

    logging.debug("Task finish: %s" % status)
