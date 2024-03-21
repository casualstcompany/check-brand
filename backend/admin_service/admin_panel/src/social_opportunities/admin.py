from django.contrib import admin

from .models import (
    ApplicationService,
    Company,
    Contacts,
    ReviewCompanyModerator,
    ReviewServiceModerator,
    Service,
    ServiceCollection,
    UsedService,
    Cooperation,
)


class ContactsInline(admin.StackedInline):
    model = Contacts
    extra = 0


class ServiceCollectionInline(admin.TabularInline):
    model = ServiceCollection
    extra = 0


class ReviewServiceModeratorInline(admin.TabularInline):
    model = ReviewServiceModerator
    extra = 0


class ReviewCompanyModeratorInline(admin.TabularInline):
    model = ReviewCompanyModerator
    extra = 0


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "logo", "owner", "status_moderator")
    list_filter = ("status_moderator",)
    search_fields = ("name", "owner")


@admin.register(UsedService)
class UsedServiceAdmin(admin.ModelAdmin):
    list_display = ("owner", "service", "status")
    list_filter = ("status",)
    search_fields = ("owner",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("company", "type", "preview", "status_moderator", "active")
    list_filter = ("type", "status_moderator", "active")
    search_fields = ("company__name",)
    autocomplete_fields = ("company",)
    inlines = [
        ContactsInline,
        ServiceCollectionInline,
        ReviewServiceModeratorInline,
    ]


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = (
        "service",
        "country",
        "state",
        "city",
        "address",
        "site",
        "phone",
        "email",
        "social",
    )
    search_fields = ("service__company__name",)


@admin.register(ReviewServiceModerator)
class ReviewServiceModeratorAdmin(admin.ModelAdmin):
    list_display = ("service", "title", "moderator", "wallet")
    search_fields = ("service__company__name", "title", "moderator")
    autocomplete_fields = ("service",)


@admin.register(ReviewCompanyModerator)
class ReviewCompanyModeratorAdmin(admin.ModelAdmin):
    list_display = ("company", "title", "moderator", "wallet")
    search_fields = ("company__name", "title", "moderator")
    autocomplete_fields = ("company",)


@admin.register(Cooperation)
class CooperationAdmin(admin.ModelAdmin):
    list_display = ("status", "site", "name", "email", "phone")
    search_fields = ("site", "email", "name")
    list_filter = ("status",)


@admin.register(ApplicationService)
class ApplicationServiceAdmin(admin.ModelAdmin):
    list_display = ("status", "service", "owner", "email")
    search_fields = ("service", "email", "owner")
    list_filter = ("status",)
