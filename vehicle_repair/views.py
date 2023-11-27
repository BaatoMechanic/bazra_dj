from typing import Any, Dict

from rest_framework.viewsets import ModelViewSet

from utils.mixins.base_api_mixin import BaseAPIMixin
from vehicle_repair.models import VehicleRepairRequest
from vehicle_repair.models.vehicle_repair_request import VehicleRepairRequestImage, VehicleRepairRequestVideo
from vehicle_repair.serializers import VehicleRepairRequestImageSerializer, VehicleRepairRequestSerializer, VehicleRepairRequestVideoSerializer
# Create your views here.


class VehicleRepairRequestViewSet(BaseAPIMixin, ModelViewSet):

    queryset = VehicleRepairRequest.objects.select_related('user').all()
    serializer_class = VehicleRepairRequestSerializer

    def get_serializer_context(self) -> Dict[str, Any]:
        return {"request": self.request}


class VehicleRepairRequestImageViewSet(BaseAPIMixin, ModelViewSet):

    queryset = VehicleRepairRequestImage.objects.all()
    serializer_class = VehicleRepairRequestImageSerializer

    def get_queryset(self):
        return VehicleRepairRequestImage.objects.filter(repair_request_id=self.kwargs["repair_request_pk"])


class VehicleRepairRequestVideoViewSet(BaseAPIMixin, ModelViewSet):

    queryset = VehicleRepairRequestVideo.objects.all()
    serializer_class = VehicleRepairRequestVideoSerializer

    def get_queryset(self):
        return VehicleRepairRequestVideo.objects.filter(repair_request_id=self.kwargs["repair_request_pk"])
