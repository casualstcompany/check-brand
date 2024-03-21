from django.contrib import admin
from django.utils import timezone

from .models import (
    Account,
    Blockchain,
    Collection,
    CurrencyToken,
    LevelsStats,
    Pack,
    Page,
    Properties,
    SmartContract,
    Token,
)


@admin.action(description="Скрыть объекты")
def hide_objects(modeladmin, request, queryset):
    queryset.update(hide=True, updated_at=timezone.now())
    modeladmin.message_user(request, "Указанные объекты были скрыты.")


class DeleteNotAllowedModelAdmin(admin.ModelAdmin):
    actions = [hide_objects]

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Token)
class TokenAdmin(DeleteNotAllowedModelAdmin):
    list_display = ["name", "collection", "number", "hide"]
    list_filter = ["collection__name", "hide"]


@admin.register(Collection)
class CollectionAdmin(DeleteNotAllowedModelAdmin):
    pass


@admin.register(Account)
class AccountAdmin(DeleteNotAllowedModelAdmin):
    pass


@admin.register(Blockchain)
class BlockchainAdmin(DeleteNotAllowedModelAdmin):
    pass


@admin.register(CurrencyToken)
class CurrencyTokenAdmin(DeleteNotAllowedModelAdmin):
    pass


@admin.register(LevelsStats)
class LevelsStatsAdmin(DeleteNotAllowedModelAdmin):
    pass


@admin.register(Pack)
class PackAdmin(DeleteNotAllowedModelAdmin):
    pass


@admin.register(Page)
class PageAdmin(DeleteNotAllowedModelAdmin):
    pass


@admin.register(Properties)
class PropertiesAdmin(DeleteNotAllowedModelAdmin):
    pass


@admin.register(SmartContract)
class SmartContractAdmin(DeleteNotAllowedModelAdmin):
    pass
