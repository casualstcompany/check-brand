import logging
import requests
import hashlib
from typing import List

from django.conf import settings
from django.utils import timezone

from billing.models import Order
from billing.settings import billing_settings

from nft_tokens.models import Token


class TinkoffService:
    url = "https://securepay.tinkoff.ru/v2/Init"

    def init_payment(self, email: str, tokens: List[Token]):
        """
        Инициализирует платеж.
        В случии успеха возвращает Order
        В противном случае None
        """
        data = self._get_body_init_payment(email, tokens)

        order = Order.objects.create(email=email, amount=data["Amount"])
        order.tokens.set(tokens)

        data["OrderId"] = str(order.pk)
        data["Token"] = self._generate_token_mapi_tinkoff(data=data)

        response_data = self._tinkoff_init(data)

        if response_data:
            order.status = response_data["Status"]
            order.payment_id = response_data["PaymentId"]
            order.payment_url = response_data["PaymentURL"]
            order.save()
            return order

        return None

    def accept_notification(self, data):
        token = data.pop("Token")
        hash = self._generate_token_mapi_tinkoff(data)

        if token == hash:
            try:
                order = Order.objects.get(
                    id=data.get("OrderId"),
                    amount=data.get("Amount"),
                    payment_id=str(data.get("PaymentId")),
                )
            except Order.DoesNotExist:
                return False
            order.status = data.get("Status")
            order.save()
            if order.status == "CONFIRMED":
                order.tokens.all().update(
                    paid=True, email=order.email, updated_at=timezone.now()
                )
            return True
        return False

    def _get_body_init_payment(self, email, tokens):
        """
        Формирует тело запроса для tinkoff api
        """
        data = {
            "TerminalKey": billing_settings.TINKOFF_TERMINAL_KEY,
            "Description": tokens[0].name,
            "SuccessURL": f"{settings.HTTP_PROTOCOL}://{settings.DOMAIN}/token/{tokens[0].id}/success",
            "NotificationURL": billing_settings.TINKOFF_NOTIFICATION_URL,
            "DATA": {"Email": email},
            "Receipt": {
                "Email": email,
                "Taxation": "osn",
            },
        }

        items = []
        total_amount = 0
        for obj in tokens:
            items.append(
                {
                    "Name": obj.name,
                    "Price": int(obj.price),
                    "Quantity": 1,
                    "Amount": int(obj.price),
                    "Tax": "none",
                }
            )
            total_amount += int(obj.price)

        data["Receipt"]["Items"] = items
        data["Amount"] = total_amount

        return data

    def _tinkoff_init(self, payload: dict):
        """Делает запрос к tinkoff API"""
        headers = {"Content-Type": "application/json"}
        logging.info(payload)
        response = requests.request(
            "POST", self.url, json=payload, headers=headers
        )
        logging.debug(response.text)
        if response.status_code != 200:
            return None

        response_data = response.json()

        if not response_data["Success"]:
            return None

        return response_data

    def _dict_to_list_key_value(self, data: dict):
        """
        Перегоняет dict в list(ключ значений)
        Исключает под словари и под списки
        """
        list_key_value: List[dict] = []

        for key, value in data.items():
            if isinstance(value, bool):
                if value:
                    list_key_value.append({key: "true"})
                else:
                    list_key_value.append({key: "false"})

            elif isinstance(value, (float, str, int)):
                list_key_value.append({key: value})

        return list_key_value

    def _generate_token_mapi_tinkoff(self, data: dict):
        """
        Генерирует из словаря хэш, добавляя пароль
        """
        list_key_value = self._dict_to_list_key_value(data)

        list_key_value.append({"Password": billing_settings.TINKOFF_PASSWORD})

        list_key_value = sorted(
            list_key_value, key=lambda x: list(x.keys())[0]
        )

        concatenated_string = "".join(
            [str(list(item.values())[0]) for item in list_key_value]
        )
        hashed_string = hashlib.sha256(
            concatenated_string.encode()
        ).hexdigest()

        return hashed_string
