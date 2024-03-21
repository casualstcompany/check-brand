import asyncio
import logging

import aio_pika

from components import admin_grpc
from core.config import get_settings as settings
from core.utils import decode_message, validation_model
from models.messages import QueueMessage
from services.smtp_service import get_smtp_service as smtp_service


class BrokerService:
    model = QueueMessage

    async def get_valid_model(self, message: aio_pika.abc.AbstractIncomingMessage):
        message_body = await decode_message(message.body)
        valid_model = validation_model(self.model, message_body)

        if not valid_model:
            return False

        return valid_model

    @staticmethod
    async def message_ack_or_reject(message: aio_pika.abc.AbstractIncomingMessage,
                                    ack: bool = False, reject: bool = True):
        logging.debug("message_ack(%s)_or_reject(%s)" % (ack, reject))
        if ack:
            await message.ack()
        else:
            await message.reject(requeue=reject)

    async def process_message(self, message: aio_pika.abc.AbstractIncomingMessage, ) -> None:

        await asyncio.sleep(settings.BROKER_MESSAGE.TIME_SLEEP)

        model = await self.get_valid_model(message)

        if not model:
            logging.error("invalid message %r" % message)
            await self.message_ack_or_reject(message, reject=False)
            return
        logging.debug("message getter")
        template_mail, template_mail_error = await admin_grpc.admin_grpc_client.get_template_mail(
            content_type=model.content_type
        )

        if not template_mail:
            logging.error("invalid template_mail for message= %r" % message.message_id)
            logging.error("error getting template = %s for message= %s" % (template_mail_error, message.message_id))
            reject = False

            if template_mail_error == "UNAVAILABLE":
                reject = True

            await self.message_ack_or_reject(message, reject=reject)
            return
        logging.debug("template getter")
        try:
            await smtp_service.send_mail(message_data=model, admin_data=template_mail)
        except Exception as e:
            logging.error("e - %s" % e)
            await self.message_ack_or_reject(message, reject=False)
            return

        await self.message_ack_or_reject(message, ack=True)


get_broker_service = BrokerService()
