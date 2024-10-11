from rest_framework.viewsets import ModelViewSet
from utils.mixins.api_mixins import BaseAPIMixin
from vehicle_repair.models import Service
from vehicle_repair.serializers import ServiceSerializer


class ServiceViewSet(BaseAPIMixin, ModelViewSet):

    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
