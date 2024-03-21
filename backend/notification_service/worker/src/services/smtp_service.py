import logging
from typing import List

import requests
from jinja2 import Template

from core.config import get_settings as settings


class SMTPService:

    @staticmethod
    async def _send_to_delivery_service(to_address: List[str], subject: str,
                                        body_html: str, body_text: str, payload: dict):

        html_template = Template(body_html).render(**payload)
        requests.post(
            f"{settings.EMAIL_DELIVERY.BASE_URL}/{settings.EMAIL_DELIVERY.DOMAIN_NAME}/messages",
            auth=("api", f"{settings.EMAIL_DELIVERY.API_KEY}"),
            data={"from": f"{settings.EMAIL_DELIVERY.NAME_SENDER} <{settings.EMAIL_DELIVERY.DEFAULT_FROM_EMAIL}>",
                  "to": ",".join(to_address),
                  "recipient-variables": ", ".join(['{"%s": {}}' % email for email in to_address]),
                  "subject": subject,
                  "text": body_text,
                  "html": html_template,
                  })

    async def send_mail(self, message_data, admin_data):
        logging.debug("Start Sending mail")
        await self._send_to_delivery_service(
            to_address=message_data.payload["email"],
            subject=admin_data.subject,
            body_html=admin_data.body_html,
            body_text=admin_data.body_text,
            payload=message_data.payload,
        )
        logging.debug(
            "Sending mail  model_message- %s, model_template- %s" % (message_data.content_type, admin_data.id)
        )


get_smtp_service = SMTPService()
