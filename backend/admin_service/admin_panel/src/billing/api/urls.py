from django.urls import include, path

from rest_framework import routers
from billing.api.v1.views import TokenTransactionViewSet, OwnerIncomeAPIView, WithdrawalRequestAPIView


router = routers.SimpleRouter()
router.register(r'tokens_transactions', TokenTransactionViewSet) # all routers


urlpatterns = [
    path("v1/", include("billing.api.v1.urls")),
    path('v1/', include(router.urls)),
    path('v1/owner_income/<str:owner>/', OwnerIncomeAPIView.as_view(), name='owner-income'),
    path('v1/token_withdrawal/<int:pk>/', WithdrawalRequestAPIView.as_view(), name='token-withdrawal'),
]
