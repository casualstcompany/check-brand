import datetime
import uuid

from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import UniqueConstraint, Q
from django.utils.translation import gettext_lazy as _

from nft_tokens.constants import (
    FILE_EXTENSION,
    ICON_FILE_EXTENSION,
    IMAGE_FILE_EXTENSION,
)
from nft_tokens.managers import HideManager


class StatusToken(models.TextChoices):
    """
    Стадии продажи токена
    """

    book = "book"
    mint_1 = "mint_1"
    mint_2 = "mint_2"
    stop = "stop"
    sold_out = "sold_out"


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.id)


class BaseModelAndHide(BaseModel):
    hide = models.BooleanField(_("hide"), default=False)

    objects = HideManager()

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Page(BaseModelAndHide, TimeStampedModel):
    name = models.CharField(_("name"), max_length=255, unique=True)
    number = models.PositiveIntegerField(_("number"), unique=True)
    url = models.SlugField(_("url"), max_length=30, unique=True)
    banner = models.ImageField(
        _("banner"),
        validators=[FileExtensionValidator(IMAGE_FILE_EXTENSION)],
        upload_to="pages/",
    )
    icon = models.FileField(
        _("icon"),
        validators=[FileExtensionValidator(ICON_FILE_EXTENSION)],
        upload_to="pages/",
        blank=True,
        null=True,
    )
    title_1 = models.CharField(_("title_1"), max_length=255)
    description = models.TextField(_("description"))
    title_2 = models.CharField(_("title_2"), max_length=255)

    class Meta:
        verbose_name = _("page")
        verbose_name_plural = _("pages")
        db_table = 'content"."page'


class TypeToken(models.TextChoices):
    """
    Предусмотрен для дальнейшего расширения токенов
    """

    standard = "standard", "Стандартный"


class SocialNetworkModel(models.Model):
    """
    Ссылки соц сетей для аккаунта и коллекций
    """

    link_opensea = models.CharField(
        _("link_opensea"), max_length=255, blank=True, null=True
    )
    link_discord = models.CharField(
        _("link_discord"), max_length=255, blank=True, null=True
    )
    link_instagram = models.CharField(
        _("link_instagram"), max_length=255, blank=True, null=True
    )
    link_medium = models.CharField(
        _("link_medium"), max_length=255, blank=True, null=True
    )
    link_twitter = models.CharField(
        _("link_twitter"), max_length=255, blank=True, null=True
    )

    class Meta:
        abstract = True


class Account(BaseModelAndHide, TimeStampedModel, SocialNetworkModel):
    page = models.ForeignKey(Page, on_delete=models.PROTECT)
    type = models.CharField(
        max_length=20,
        verbose_name=_("type"),
        choices=TypeToken.choices,
        default=TypeToken.standard,
    )
    logo = models.ImageField(
        _("logo"),
        validators=[FileExtensionValidator(IMAGE_FILE_EXTENSION)],
        upload_to="accounts/",
    )
    cover = models.ImageField(
        _("cover"),
        validators=[FileExtensionValidator(IMAGE_FILE_EXTENSION)],
        upload_to="accounts/",
    )
    banner = models.ImageField(
        _("banner"),
        validators=[FileExtensionValidator(IMAGE_FILE_EXTENSION)],
        upload_to="accounts/",
    )
    name = models.CharField(_("name"), max_length=255, unique=True)
    url = models.SlugField(_("url"), max_length=30, unique=True)
    description = models.TextField(_("description"))

    items_count = models.PositiveIntegerField(_("items count"), default=0)
    owners_count = models.PositiveIntegerField(_("owners count"), default=0)
    collections_count = models.PositiveIntegerField(
        _("collections count"), default=0
    )

    floor_price_count = models.DecimalField(
        _("floor_price_count"), decimal_places=8, max_digits=15, default=0
    )
    volume_troded_count = models.DecimalField(
        _("volume_troded_count"), decimal_places=8, max_digits=15, default=0
    )
    profit = models.DecimalField(
        _("profit"), decimal_places=8, max_digits=15, default=0
    )

    class Meta:
        verbose_name = _("account")
        verbose_name_plural = _("accounts")
        db_table = 'content"."account'


class Blockchain(BaseModel, TimeStampedModel):
    name = models.CharField(_("name"), max_length=255, unique=True)

    class Meta:
        verbose_name = _("blockchain")
        verbose_name_plural = _("blockchains")
        db_table = 'content"."blockchain'


class SmartContract(BaseModel, TimeStampedModel):
    administrator_address = models.CharField(
        _("administrator_address"), max_length=255
    )
    address = models.CharField(_("address"), max_length=255)

    class Meta:
        verbose_name = _("smart contract")
        verbose_name_plural = _("smart contracts")
        db_table = 'content"."smart_contract'
        unique_together = (("administrator_address", "address"),)


class Collection(BaseModelAndHide, TimeStampedModel, SocialNetworkModel):
    page = models.ForeignKey(Page, on_delete=models.PROTECT)
    application_form = models.CharField(
        _("application form"), max_length=255, default="basic"
    )
    account = models.ForeignKey(Account, on_delete=models.PROTECT)

    type = models.CharField(
        max_length=20,
        verbose_name=_("type"),
        choices=TypeToken.choices,
        default=TypeToken.standard,
    )

    logo = models.ImageField(
        _("logo"),
        validators=[FileExtensionValidator(IMAGE_FILE_EXTENSION)],
        upload_to="collections/",
    )

    featured = models.ImageField(
        _("featured"),
        validators=[FileExtensionValidator(IMAGE_FILE_EXTENSION)],
        upload_to="collections/",
    )

    banner = models.ImageField(
        _("banner"),
        validators=[FileExtensionValidator(IMAGE_FILE_EXTENSION)],
        upload_to="collections/",
    )

    name = models.CharField(_("name"), max_length=255, unique=True)
    url = models.SlugField(_("url"), max_length=50, unique=True)
    symbol = models.SlugField(_("symbol"), max_length=7, unique=True)
    url_opensea = models.CharField(
        _("url_opensea"), max_length=255, blank=True, null=True
    )
    percentage_fee = models.DecimalField(
        _("percentage_fee"), decimal_places=8, max_digits=15
    )
    display_theme = models.CharField(_("display_theme"), max_length=50)
    description = models.TextField(_("description"))

    blockchain = models.ForeignKey(Blockchain, on_delete=models.PROTECT)
    upload_blockchain = models.BooleanField(
        _("upload_blockchain"), default=False
    )

    smart_contract_address = models.CharField(
        _("smart_contract_address"), max_length=255, blank=True, null=True
    )

    items_count = models.PositiveIntegerField(_("items count"), default=0)
    owners_count = models.PositiveIntegerField(_("owners count"), default=0)

    floor_price_count = models.DecimalField(
        _("floor_price_count"), decimal_places=8, max_digits=15, default=0
    )
    volume_troded_count = models.DecimalField(
        _("volume_troded_count"), decimal_places=8, max_digits=15, default=0
    )
    profit = models.DecimalField(
        _("profit"), decimal_places=8, max_digits=15, default=0
    )

    creator_profit = models.DecimalField(
        _("creator profit"), decimal_places=8, max_digits=15, default=0
    )
    creator_fee = models.DecimalField(
        _("creator fee"), decimal_places=8, max_digits=15, default=0
    )

    payment_tokens = models.ManyToManyField(
        "CurrencyToken", related_name="collection"
    )

    status = models.CharField(
        max_length=20,
        verbose_name=_("status"),
        choices=StatusToken.choices,
        default=StatusToken.stop,
    )

    class Meta:
        verbose_name = _("collection")
        verbose_name_plural = _("collections")
        db_table = 'content"."collection'


class StatusPriceToken(models.TextChoices):
    """
    Определяет будет ли показана цена
    """

    auction = "auction", "Аукцион"
    no_price = "no_price", "Цена не указана"
    price = "price", "Цена указана"


class CurrencyToken(BaseModel, TimeStampedModel):
    name = models.CharField(_("name"), max_length=10, unique=True)
    blockchain = models.ForeignKey(Blockchain, on_delete=models.PROTECT)
    smart_contract_address = models.CharField(
        _("smart contract address"), max_length=255
    )

    class Meta:
        verbose_name = _("currency_token")
        verbose_name_plural = _("currency_tokens")
        db_table = 'content"."currency_token'


class TemplatePackAndToken(BaseModelAndHide, TimeStampedModel):
    block = models.BooleanField(_("block"), default=False)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)

    type = models.CharField(
        max_length=20,
        verbose_name=_("type"),
        choices=TypeToken.choices,
        default=TypeToken.standard,
    )
    name = models.CharField(_("name"), max_length=255)

    price = models.PositiveIntegerField(
        _("price"),
        help_text="Цена в копейках",
    )
    currency_token = models.ForeignKey(CurrencyToken, on_delete=models.PROTECT)

    status_price = models.CharField(
        max_length=10,
        verbose_name=_("status price"),
        choices=StatusPriceToken.choices,
        default=StatusPriceToken.price,
    )

    investor_royalty = models.DecimalField(
        _("investor royalty"), decimal_places=8, max_digits=15
    )
    creator_royalty = models.DecimalField(
        _("creator royalty"), decimal_places=8, max_digits=15
    )

    description = models.TextField(_("description"))

    close = models.BooleanField(_("close"), default=False)
    close_image = models.ImageField(
        _("close image"),
        blank=True,
        null=True,
        validators=[FileExtensionValidator(IMAGE_FILE_EXTENSION)],
        upload_to="packs/",
    )

    unlockable = models.BooleanField(_("unlockable"), default=False)
    unlockable_content = models.TextField(
        _("unlockable content"), blank=True, null=True
    )

    upload_blockchain = models.BooleanField(
        _("upload blockchain"), default=False
    )

    status = models.CharField(
        max_length=20,
        verbose_name=_("status"),
        choices=StatusToken.choices,
        default=StatusToken.stop,
    )

    freeze = models.BooleanField(_("freeze"), default=False)

    wallet_owner = models.CharField(
        _("wallet_owner"), max_length=255, blank=True, null=True
    )

    class Meta:
        abstract = True


class Pack(TemplatePackAndToken):
    items_count = models.PositiveIntegerField(_("items count"), default=0)
    profit = models.DecimalField(
        _("profit"), decimal_places=8, max_digits=15, default=0
    )

    properties = models.ManyToManyField(
        "Properties", related_name="pack", blank=True
    )
    levels_stats = models.ManyToManyField(
        "LevelsStats", related_name="pack", blank=True
    )
    creator_royalty_distribution = models.ManyToManyField(
        "CreatorRoyaltyDistribution", related_name="pack", blank=True
    )
    income_distribution = models.ManyToManyField(
        "IncomeDistribution", related_name="pack", blank=True
    )

    status_duration_date = models.DateField(
        _("status_duration"), default=datetime.date.today
    )

    class Meta:
        verbose_name = _("pack")
        verbose_name_plural = _("packs")
        db_table = 'content"."pack'
        constraints = [
            UniqueConstraint(
                fields=["collection", "name"],
                condition=Q(hide=False),
                name="pack_uniq_name_and_collection",
                violation_error_message=(
                    "Пакет с таким именем в выбранной коллекции уже"
                    " существует."
                ),
            )
        ]


class Token(TemplatePackAndToken):
    address = models.CharField(
        _("address"), max_length=255, blank=True, null=True
    )
    pack = models.ForeignKey(
        Pack, on_delete=models.PROTECT, related_name="token"
    )
    number = models.PositiveIntegerField(
        editable=False, verbose_name="number", blank=True, null=True
    )

    file_1 = models.FileField(
        _("file_1"),
        validators=[FileExtensionValidator(FILE_EXTENSION)],
        max_length=150,
    )
    file_2 = models.FileField(
        _("file_2"),
        validators=[FileExtensionValidator(FILE_EXTENSION)],
        max_length=150,
    )

    file_1_name_ext = models.CharField(
        _("file_1_name_ext"), max_length=150, blank=True, null=True
    )
    file_2_name_ext = models.CharField(
        _("file_2_name_ext"), max_length=150, blank=True, null=True
    )

    url_opensea = models.CharField(
        _("url_opensea"), max_length=255, blank=True, null=True
    )

    mint = models.BooleanField(_("mint"), default=False)
    paid = models.BooleanField(_("paid"), default=False)
    email = models.EmailField(
        verbose_name="Email владельца", blank=True, null=True
    )

    profit = models.DecimalField(
        _("profit"), decimal_places=8, max_digits=15, default=0
    )

    properties = models.ManyToManyField(
        "Properties", related_name="token", blank=True
    )
    levels_stats = models.ManyToManyField(
        "LevelsStats", related_name="token", blank=True
    )
    creator_royalty_distribution = models.ManyToManyField(
        "CreatorRoyaltyDistribution", related_name="token", blank=True
    )
    income_distribution = models.ManyToManyField(
        "IncomeDistribution", related_name="token", blank=True
    )

    class Meta:
        verbose_name = _("token")
        verbose_name_plural = _("tokens")
        db_table = 'content"."token'
        constraints = [
            UniqueConstraint(
                fields=["collection", "name"],
                condition=Q(hide=False),
                name="token_uniq_name_and_collection",
                violation_error_message=(
                    "Сертификат с таким именем в выбранной коллекции уже"
                    " существует."
                ),
            ),
            UniqueConstraint(
                fields=["collection", "number"],
                condition=Q(hide=False),
                name="token_uniq_number_and_collection",
                violation_error_message=(
                    "Сертификат с таким номером в выбранной коллекции уже"
                    " существует."
                ),
            ),
        ]


class TypeLevelsStats(models.TextChoices):
    levels = "levels"
    stats = "stats"


class LevelsStats(BaseModel, TimeStampedModel):
    name = models.CharField(_("name"), max_length=50)
    type = models.CharField(
        max_length=6,
        verbose_name=_("type"),
        choices=TypeLevelsStats.choices,
    )
    value_1 = models.PositiveIntegerField(_("value_1"))
    value_2 = models.PositiveIntegerField(_("value_2"))

    class Meta:
        verbose_name = _("levels_stats")
        verbose_name_plural = _("levels_stats")
        db_table = 'content"."levels_stats'


class Properties(BaseModel, TimeStampedModel):
    name = models.CharField(_("name"), max_length=256)
    type = models.CharField(_("type"), max_length=50)

    class Meta:
        verbose_name = _("properties")
        verbose_name_plural = _("properties")
        db_table = 'content"."properties'


class CreatorRoyaltyDistribution(BaseModel, TimeStampedModel):
    wallet = models.CharField(_("wallet"), max_length=255)
    percent = models.DecimalField(
        _("percent"), decimal_places=8, max_digits=15, default=0
    )

    class Meta:
        verbose_name = _("creator royalty distribution")
        verbose_name_plural = _("creator royalty distributions")
        db_table = 'content"."creator_royalty_distribution'


class IncomeDistribution(BaseModel, TimeStampedModel):
    wallet = models.CharField(_("wallet"), max_length=255)
    percent = models.DecimalField(
        _("percent"), decimal_places=8, max_digits=15, default=0
    )

    class Meta:
        verbose_name = _("income distribution")
        verbose_name_plural = _("income distributions")
        db_table = 'content"."income_distribution'
