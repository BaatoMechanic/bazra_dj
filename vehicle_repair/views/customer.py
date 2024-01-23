from rest_framework.viewsets import ModelViewSet, GenericViewSet

from utils.mixins.base_api_mixin import BaseAPIMixin
from rest_framework.mixins import RetrieveModelMixin
from vehicle_repair.models.customer import Customer

from vehicle_repair.serializers.customer import CustomerSerializer


class CustomerViewSet(BaseAPIMixin, RetrieveModelMixin, GenericViewSet):

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
