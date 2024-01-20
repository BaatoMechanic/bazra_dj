
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from utils.mixins.base_api_mixin import BaseAPIMixin
from vehicle_repair.models import Service
from vehicle_repair.models.vehicle_repair_request import VehicleRepairRequest
from vehicle_repair.serializers import ServiceSerializer

# Create your views here.


class ServiceViewSet(BaseAPIMixin, ModelViewSet):

    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
