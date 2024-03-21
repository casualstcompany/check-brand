from django.contrib import admin
from .models import Order,TokenTransaction,TransactionLog


class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "amount", "email", "payment_id", "status")
    list_filter = ("status",)
    search_fields = ("email", "payment_id")


admin.site.register(Order, OrderAdmin)
admin.site.register(TokenTransaction)
