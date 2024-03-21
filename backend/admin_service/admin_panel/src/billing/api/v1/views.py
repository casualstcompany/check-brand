from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_yasg.utils import swagger_auto_schema

from billing.serializers import CreateOrderSerializer, ResponsePayments, TokenTransactionSerializer
from billing.service import TinkoffService

from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import GenericViewSet

from rest_framework import generics, mixins
from billing.models import TokenTransaction

from nft_tokens.pagination import StandardResultsSetPagination





class CreatePaymentView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CreateOrderSerializer

    @swagger_auto_schema(
        request_body=CreateOrderSerializer, responses={201: ResponsePayments}
    )
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.check_exists():
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )

        payment_service = TinkoffService()
        response_data = payment_service.init_payment(
            email=serializer.validated_data["email"],
            tokens=serializer.validated_data["tokens"],
        )
        if not response_data:
            return Response(
                {
                    "non_field_errors": [
                        "Платеж не удалось инициализировать, пожалуйста,"
                        " повторите попытку позже."
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            self.serializer_class(instance=response_data).data,
            status=status.HTTP_201_CREATED,
        )


class UpdateStatusOrderView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        payment_service = TinkoffService()
        if payment_service.accept_notification(request.data):
            return Response(
                "OK",
                status=status.HTTP_200_OK,
            )

        return Response(
            status=status.HTTP_404_NOT_FOUND,
        )


class TokenTransactionViewSet(mixins.CreateModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.ListModelMixin,
                              GenericViewSet):
                              
    queryset = TokenTransaction.objects.all()
    serializer_class = TokenTransactionSerializer
    pagination_class = StandardResultsSetPagination
    http_method_names = ['get', 'post', 'patch']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        status_param = request.query_params.get('status', None)
        if status_param:
            queryset = queryset.filter(status=status_param)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = TokenTransaction.objects.all()
        token = get_object_or_404(queryset, pk=pk)
        serializer = TokenTransaction(token)
        return Response({"data": serializer.data})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"data": serializer.data})

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"data": serializer.data})
    


class OwnerIncomeAPIView(generics.ListAPIView):
    serializer_class = TokenTransactionSerializer

    def get_queryset(self):
        owner = self.kwargs['owner']
        return TokenTransaction.objects.filter(owner=owner)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        total_income = sum([(obj.amount * 0.96) - (obj.withdrawal / 2) for obj in queryset])
        return Response({'total_income': total_income})
    

class WithdrawalRequestAPIView(generics.UpdateAPIView):
    serializer_class = TokenTransactionSerializer

    def update(self, request, *args, **kwargs):
        token_id = kwargs.get('pk')
        withdrawal_amount = request.data.get('withdrawal_amount')

        try:
            token_transaction = TokenTransaction.objects.get(tokens=token_id)
        except TokenTransaction.DoesNotExist:
            return Response({"error": "Транзакция токена не найдена"}, status=status.HTTP_404_NOT_FOUND)

        if withdrawal_amount > token_transaction.to_withdraw:
            return Response({"error": "Запрашиваемая сумма для вывода превышает доступную сумму для вывода"}, status=status.HTTP_400_BAD_REQUEST)

        withdrawal_amount_half = withdrawal_amount / 2

        token_transaction.withdrawal = withdrawal_amount_half
        token_transaction.save()

        serializer = self.get_serializer(token_transaction)
        return Response(serializer.data)
