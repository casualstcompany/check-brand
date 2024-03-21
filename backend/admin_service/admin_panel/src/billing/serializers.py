from collections import OrderedDict
from datetime import datetime, timedelta
import re

from rest_framework import serializers

from billing.models import Order, TokenTransaction
from billing.settings import billing_settings


class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            "id",
            "email",
            "tokens",
        )

    def validate_email(self, value):
        email_regex = re.compile(
            r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        )

        if not email_regex.match(value):
            raise serializers.ValidationError(
                ["Неверный адрес электронной почты"],
            )
        return value.lower()

    def validate_tokens(self, value):

        if Order.objects.filter(status="CONFIRMED", tokens__in=value).exists():
            raise serializers.ValidationError(f"Сертификат уже куплен")

        return value

    def check_exists(self):
        objs = self.Meta.model.objects.filter(
            status="NEW",
            created_at__gt=(
                datetime.now()
                - timedelta(
                    minutes=int(billing_settings.TINKOFF_LIFETIME_LINK_MUNUTES)
                )
            ),
            email=self.validated_data["email"],
            tokens__in=self.validated_data["tokens"],
        )
        if objs.exists():
            self.instance = objs.first()
            return True

        return False

    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """
        ret = OrderedDict()
        ret["order_id"] = instance.pk
        ret["status"] = instance.status
        ret["amount"] = instance.amount
        ret["payment_url"] = instance.payment_url

        return ret


class ResponsePayments(serializers.Serializer):
    order_id = serializers.UUIDField()
    status = serializers.CharField()
    amount = serializers.IntegerField()
    paument_url = serializers.CharField()

    
class TokenTransactionSerializer(serializers.ModelSerializer):
    to_return = serializers.SerializerMethodField()

    class Meta:
        model = TokenTransaction
        fields = ['id', 'tokens', 'amount', 'status', 'accrual', 'withdrawal', 'to_withdraw', 'to_return', 'owner', 'email', 'date']

    def get_to_return(self, obj):
        return ((obj.amount * 0.96) - (obj.withdrawal / 2))

