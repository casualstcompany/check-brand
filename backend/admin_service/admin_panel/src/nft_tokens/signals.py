import logging

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from nft_tokens import tasks
from nft_tokens.models import Collection, Pack, Token
from nft_tokens.services import (
    CollectionService,
    PackService,
    pack_update,
    status_update_in_collection,
)

logger = logging.getLogger(__name__)


@receiver(status_update_in_collection, sender=CollectionService)
def get_signal_status_update_in_collection(sender, collection_id, **kwargs):
    """Получаем сигнал и создаём задачу"""
    logger.debug("Signal received  -  status update in collection.")
    tasks.task_status_update_in_collection.delay(collection_id)


@receiver(pack_update, sender=PackService)
def get_signal_update_pack(sender, pack_id, update_fields, **kwargs):
    """Получаем сигнал и создаём задачу
    на обновление полей у токена по пакету
    и на обновление полей у моделей выше
    """
    logger.debug("Signal received  -  pack updated")
    tasks.task_update_tokens_pack_collection_account.delay(
        pack_id, status="pack_updated"
    )


@receiver(post_save, sender=Token)
def update_pack_collection_account_counted_fields(
    sender, instance, created, **kwargs
):
    logger.debug("Signal received  -  token updated/created")

    status = "token_updated"
    if created:
        status = "token_created"

    tasks.task_update_tokens_pack_collection_account.delay(
        pack_id=instance.pack.id, status=status
    )


@receiver(post_save, sender=Collection)
def update_account_counted_fields(sender, instance, created, **kwargs):
    if created:
        logger.debug("Signal received  -  collection created")
        tasks.task_update_account.delay(
            account_id=instance.account.id, status="collection_created"
        )


@receiver(post_delete, sender=Token)
def post_delete_update_pack_collection_account_counted_fields(
    sender, instance, **kwargs
):
    logger.info("Signal received  -  token deleted")

    tasks.task_update_tokens_pack_collection_account.delay(
        pack_id=instance.pack.id, status="token_deleted"
    )


@receiver(post_delete, sender=Pack)
def post_delete_update_collection_account_counted_fields(
    sender, instance, **kwargs
):
    logger.info("Signal received  -  pack deleted")

    tasks.task_update_collection_account.delay(
        instance.collection.id, status="pack_deleted"
    )


@receiver(post_delete, sender=Collection)
def post_delete_update_account_counted_fields(sender, instance, **kwargs):
    logger.info("Signal received  -  collection deleted")
    tasks.task_update_account.delay(
        account_id=instance.account.id, status="collection_deleted"
    )
