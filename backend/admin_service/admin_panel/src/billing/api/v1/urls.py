from django.urls import path

from billing.api.v1.views import CreatePaymentView, UpdateStatusOrderView

urlpatterns = [
    path("payments", CreatePaymentView.as_view()),
    path("payments/notification", UpdateStatusOrderView.as_view()),
]
