import uuid
from django.db import models
from django.core.validators import FileExtensionValidator
from django.db.models import UniqueConstraint

from nft_tokens.models import Collection, Token
from nft_tokens.constants import IMAGE_FILE_EXTENSION
from tools.models import BaseModel, TimeStampedModel


class TypeServiceChoices(models.TextChoices):
    PASS_TO = "pass_to", "Pass To"
    VIP_SERVICE = "vip_service", "VIP Service"
    DISCOUNT = "discount", "Discount"
    GIFT = "gift", "Gift"


class CertificateTypeServiceChoices(models.TextChoices):
    UNIQUE = "unique", "Unique"
    PREMIUM = "premium", "Premium"
    VIP = "vip", "VIP"


class StatusModeratorChoices(models.TextChoices):
    PENDING = "pending", "Pending"
    CORRECT = "correct", "Correct"
    APPROVED = "approved", "Approved"
    BLOCKED = "blocked", "Blocked"


class Company(BaseModel, TimeStampedModel, models.Model):
    name = models.CharField(max_length=30, unique=True)
    logo = models.ImageField(
        "Лого",
        validators=[FileExtensionValidator(IMAGE_FILE_EXTENSION)],
        upload_to="company/",
    )
    owner = models.CharField(max_length=255)
    status_moderator = models.CharField(
        max_length=15,
        choices=StatusModeratorChoices.choices,
        default=StatusModeratorChoices.CORRECT,
    )

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "1 - Компания"
        verbose_name_plural = "1 - Компании"
        db_table = 'social_opportunities"."company'

    def __str__(self):
        return self.name


class Service(BaseModel, TimeStampedModel, models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="services",
    )
    type = models.CharField(
        max_length=50,
        choices=TypeServiceChoices.choices,
        default=TypeServiceChoices.VIP_SERVICE,
    )
    certificate_type = models.CharField(
        max_length=50,
        choices=CertificateTypeServiceChoices.choices,
        default=CertificateTypeServiceChoices.UNIQUE,
    )
    preview = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    status_moderator = models.CharField(
        max_length=15,
        choices=StatusModeratorChoices.choices,
        default=StatusModeratorChoices.CORRECT,
    )
    active = models.BooleanField(default=True)

    collections = models.ManyToManyField(
        Collection, through="ServiceCollection"
    )

    manager_telegram = models.CharField(max_length=255)
    manager_whatsapp = models.CharField(max_length=255)
    manager_email = models.EmailField(verbose_name="manager_email")

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "2 - Сервис"
        verbose_name_plural = "2 - Сервисы"
        db_table = 'social_opportunities"."service'

    def __str__(self):
        return str(self.id)


class ServiceCollection(BaseModel, TimeStampedModel, models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
    )
    collection = models.ForeignKey(
        Collection, on_delete=models.SET_NULL, blank=True, null=True
    )

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Коллекции сервиса"
        verbose_name_plural = "Коллекции сервисов"
        db_table = 'social_opportunities"."service_collection'

    def __str__(self):
        return str(self.id)


class Contacts(BaseModel, TimeStampedModel, models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="contacts",
    )
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    site = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    social = models.CharField(max_length=255)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "3 - Контакт"
        verbose_name_plural = "3 - Контакты"
        db_table = 'social_opportunities"."contacts'

    def __str__(self):
        return str(self.id)


class BaseReviewModel(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    moderator = models.CharField(max_length=255)
    wallet = models.CharField(max_length=255)

    class Meta:
        abstract = True


class ReviewServiceModerator(
    BaseModel, TimeStampedModel, BaseReviewModel, models.Model
):
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "5 - Отзыв сервиса"
        verbose_name_plural = "5 - Отзывы сервиса"
        db_table = 'social_opportunities"."review_service'

    def __str__(self):
        return self.title


class ReviewCompanyModerator(
    BaseModel, TimeStampedModel, BaseReviewModel, models.Model
):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "4 - Отзыв компании"
        verbose_name_plural = "4 - Отзывы компании"
        db_table = 'social_opportunities"."review_company'

    def __str__(self):
        return self.title


class UsedService(BaseModel, TimeStampedModel, models.Model):
    class StatusUsedServiceChoices(models.TextChoices):
        CLICKED = "clicked", "Clicked"
        USED = "used", "Used"
        NOT_USED = "not_used", "Not used"

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="used",
    )
    token = models.ForeignKey(
        Token, on_delete=models.SET_NULL, blank=True, null=True
    )
    owner = models.CharField(max_length=255)
    status = models.CharField(
        max_length=15,
        choices=StatusUsedServiceChoices.choices,
        default=StatusUsedServiceChoices.NOT_USED,
    )

    class Meta:
        verbose_name = "6 - Оказанная услуга"
        verbose_name_plural = "6 - Оказанные услуги"
        db_table = 'social_opportunities"."used_service'
        constraints = [
            UniqueConstraint(
                name="service_token_uniq",
                fields=["service", "token"],
            )
        ]

    def __str__(self):
        return str(self.id)


class Cooperation(BaseModel, TimeStampedModel, models.Model):
    """Предложения на сотрудничество"""

    class StatusChoices(models.TextChoices):
        VIEW = "view", "Просмотрено"
        NEW = "new", "Новое"

    email = models.EmailField(
        verbose_name="Почта", max_length=100, unique=True
    )

    name = models.CharField(verbose_name="Имя", max_length=120)
    phone = models.CharField(verbose_name="Телефон", max_length=120)
    site = models.CharField(
        verbose_name="Сайт", max_length=120, blank=True, null=True
    )

    status = models.CharField(
        max_length=15,
        choices=StatusChoices.choices,
        default=StatusChoices.NEW,
    )

    class Meta:
        verbose_name = "Предложения на сотрудничество"
        verbose_name_plural = "Предложения на сотрудничество"
        db_table = 'social_opportunities"."cooperation'

    def __str__(self):
        return self.email


class ApplicationService(BaseModel, TimeStampedModel, models.Model):
    """Заявка на сервис"""

    class StatusChoices(models.TextChoices):
        VIEW = "view", "Просмотрено"
        NEW = "new", "Новое"

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="application",
    )
    token = models.ForeignKey(
        Token,
        on_delete=models.CASCADE,
        related_name="application",
    )
    owner = models.CharField(max_length=255)
    email = models.EmailField(verbose_name="Почта", max_length=100)

    payload = models.JSONField()

    status = models.CharField(
        max_length=15,
        choices=StatusChoices.choices,
        default=StatusChoices.NEW,
    )

    class Meta:
        verbose_name = "Заявка на использование сервиса"
        verbose_name_plural = "Заявки на использование сервиса"
        db_table = 'social_opportunities"."application'

    def __str__(self):
        return self.email
