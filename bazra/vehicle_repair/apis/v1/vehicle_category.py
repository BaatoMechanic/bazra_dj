from rest_framework.viewsets import ModelViewSet

from utils.mixins.api_mixins import BaseAPIMixin

from vehicle_repair.models.vehicle_category import VehicleCategory
from vehicle_repair.serializers.vehicle_category import VehicleCategorySerializer
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.


class VehicleCategoryViewSet(BaseAPIMixin, ModelViewSet):

    queryset = VehicleCategory.objects.all()
    serializer_class = VehicleCategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["services__idx"]
