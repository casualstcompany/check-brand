import uuid

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ContentType(models.TextChoices):
    TEST = 'test'
    ADD_WHITE_LIST = 'added_white_list', 'added_white_list'
    BOOKING_STARTED = 'booking_started', 'booking_started'
    ADD_WHITE_LIST_AND_BOOK = 'added_white_list_and_booking', 'added_white_list_and_booking'
    USER_BOOK = 'user_booked', 'user_booked'
    MINT_1_START = 'minting_1_started', 'minting_1_started'
    ADD_WHITE_LIST_AND_EXPECTS = 'added_white_and_expects', 'added_white_and_expects'
    MINT_2_START = 'minting_2_started', 'minting_2_started'
    ADD_WHITE_LIST_AND_MINT_2 = 'added_white_list_and_minting_2', 'added_white_list_and_minting_2'
    USER_MINT = 'user_minted', 'user_minted'
    SOLD_OUT = 'sold_out', 'sold_out'
    # MINT_STOP = 'minting_stopped', 'minting_stopped'


class TemplateMail(BaseModel, TimeStampedModel):
    subject = models.CharField(_('subject'), max_length=255)
    body_html = models.TextField(_('body_html'))
    body_text = models.TextField(_('body_text'))
    payload = models.JSONField(_('example_payload'))
    content_type = models.CharField(
        _('content type'),
        max_length=64,
        choices=ContentType.choices,
        default=ContentType.TEST,
        unique=True
    )

    class Meta:
        verbose_name = _('template')
        verbose_name_plural = _('templates')
        db_table = "content\".\"template"

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse("template_detail", kwargs={'id': self.id})
