from django.contrib import admin

from .models import TemplateMail


@admin.register(TemplateMail)
class TemplateMailAdmin(admin.ModelAdmin):
    list_display = ("subject", "content_type",)
