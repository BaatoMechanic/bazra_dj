from django.shortcuts import get_object_or_404
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from utils.mixins.api_mixins import BaseAPIMixin
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin
from vehicle_repair.models.customer import Customer
from rest_framework.response import Response

from vehicle_repair.serializers.customer import CustomerSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomerViewSet(BaseAPIMixin, RetrieveModelMixin, CreateModelMixin, GenericViewSet):

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    # def create(self, request, *args, **kwargs):
    #     return super().create(request, *args, **kwargs)

    @action(detail=False)
    def me(self, request):
        customer = get_object_or_404(Customer, user=request.user)
        serializer = self.get_serializer(customer)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def customer_by_useridx(self, request):
        user_idx = self.request.query_params.get("user_idx", None)
        user = User.objects.get(idx=user_idx)
        customer = get_object_or_404(Customer, user=user)
        serializer = self.get_serializer(customer)
        return Response(serializer.data)
