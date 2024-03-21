from django.db import models

from nft_tokens.models import Token
from tools.models import BaseModel, TimeStampedModel

from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

class Order(TimeStampedModel, BaseModel, models.Model):
    amount = models.PositiveIntegerField(
        verbose_name="Сумма, в копейках",
        default=0,
    )
    email = models.EmailField(verbose_name="Email покупателя")
    tokens = models.ManyToManyField(
        Token, verbose_name="приобретаемые сертификаты"
    )

    payment_id = models.CharField(
        verbose_name="Идентификатор платежа в системе Тинькофф Кассы",
        max_length=20,
        blank=True,
        null=True,
    )
    payment_url = models.CharField(
        verbose_name="Ссылка на платежную форму",
        max_length=100,
        blank=True,
        null=True,
    )

    status = models.CharField(
        verbose_name="Статус транзакции", max_length=20, default="CREATED"
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        db_table = 'billing"."order'

    def __str__(self):
        return f"Order {self.pk}"
    



class TokenTransaction(models.Model):
    STATUS_CHOICES = (
        ('Withdrawal', 'Вывод'),
        ('Refund', 'Возврат'),
        ('Withdrawn', 'Выведено'),
        ('Returned', 'Возвращено'),
    )

    tokens = models.ForeignKey(Token, on_delete=models.CASCADE, verbose_name="Токен")
    amount = models.FloatField(verbose_name="Стоимость")
    profitability = models.FloatField(verbose_name='Доходность')
    status = models.CharField(verbose_name="Статус", max_length=100, choices=STATUS_CHOICES)
    accrual = models.FloatField(verbose_name="Начислено")
    max_accrual = models.FloatField(verbose_name="Максимально начисление")
    withdrawal = models.FloatField(verbose_name="Выведено")
    to_withdraw = models.FloatField(verbose_name="К выводу")
    to_return = models.FloatField(verbose_name="К возврату")
    owner = models.CharField(verbose_name="Владелец", max_length=100)
    email = models.EmailField(verbose_name="Email владельца", blank=True, null=True)
    date = models.DateTimeField(verbose_name="Дата", auto_now_add=True)

    class Meta:
        verbose_name = "Транзакция токена"
        verbose_name_plural = "Транзакции токенов"
        db_table = 'billing_token_transaction'

    def clean(self):
        if self.accrual > self.max_accrual:
            raise ValidationError({'accrual': 'Сумма начислений не должна превышать сумму максимальных начислений'})

        if self.withdrawal > self.to_withdraw:
            raise ValidationError({'withdrawal': 'Сумма вывода не должна превышать сумму к выводу'})

# Создание модели для записи журнала событий
class TransactionLog(models.Model):
    transaction = models.ForeignKey(TokenTransaction, on_delete=models.CASCADE)
    field_name = models.CharField(max_length=100)
    old_value = models.CharField(max_length=255)
    new_value = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

# Обработчик сигнала pre_save для сохранения изменений в журнале
@receiver(pre_save, sender=TokenTransaction)
def log_transaction_changes(sender, instance, **kwargs):
    if instance.pk:
        old_instance = TokenTransaction.objects.get(pk=instance.pk)
        for field in instance._meta.fields:
            old_value = getattr(old_instance, field.name)
            new_value = getattr(instance, field.name)
            if old_value != new_value and field.name in ['accrual', 'withdrawal','to_withdraw','to_return']:
                TransactionLog.objects.create(
                    transaction=instance,
                    field_name=field.name,
                    old_value=str(old_value),
                    new_value=str(new_value)
                )