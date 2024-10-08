from rest_framework.viewsets import ModelViewSet
from utils.mixins.base_api_mixin import BaseAPIMixin
from vehicle_repair.models import Service
from vehicle_repair.serializers import ServiceSerializer


class ServiceViewSet(BaseAPIMixin, ModelViewSet):

    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
