import uuid

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import ShortURL


@admin.action(
    description="Генерировать уникальные ссылки",
)
def generate_unique_url(modeladmin, request, queryset):
    for query in queryset.filter(generate=False):
        short_url = uuid.uuid4().hex[:6].upper()
        while ShortURL.objects.filter(url_hash=short_url).exists():
            short_url = uuid.uuid4().hex[:6].upper()

        query.url_hash = short_url
        query.generate = True
        query.save()


@admin.action(
    description="Сгенерировать 150 случайных",
)
def generate_new_150(modeladmin, request, queryset):
    for i in range(151):
        short_url = uuid.uuid4().hex[:6].upper()
        while ShortURL.objects.filter(url_hash=short_url).exists():
            short_url = uuid.uuid4().hex[:6].upper()
        ShortURL.objects.create(
            collection_name="default",
            token_name="default",
            full_url="http://www.checkbrand.com/",
            url_hash=short_url,
            generate=True,
        )


@admin.register(ShortURL)
class ShortURLAdmin(ImportExportModelAdmin):
    actions = [
        generate_unique_url,
        generate_new_150,
    ]
