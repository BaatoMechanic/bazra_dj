from typing import Any, Dict

from django.shortcuts import get_object_or_404

from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from utils.mixins.base_api_mixin import BaseAPIMixin
from vehicle_repair.models import VehicleRepairRequest
from vehicle_repair.models.vehicle_repair_request import VehicleRepairRequestImage, VehicleRepairRequestVideo
from vehicle_repair.serializers.service import ServiceSerializer
from vehicle_repair.serializers.vehicle_repair_request import VehicleRepairRequestImageSerializer, VehicleRepairRequestSerializer, VehicleRepairRequestVideoSerializer
# Create your views here.


class VehicleRepairRequestViewSet(BaseAPIMixin, ModelViewSet):

    queryset = VehicleRepairRequest.objects.select_related('user').all().order_by('-created_at')
    serializer_class = VehicleRepairRequestSerializer

    def get_serializer_context(self) -> Dict[str, Any]:
        return {"request": self.request}

    @action(detail=True, methods=['GET'])
    def service_type(self, request, idx):
        repair_request = get_object_or_404(VehicleRepairRequest, idx=idx)
        serializer = ServiceSerializer(repair_request.service_type)
        return Response(serializer.data)
    
    
    @action(detail=False, methods=['GET'])
    def user_recent_repair_requests(self, request):
        repair_requests = VehicleRepairRequest.objects.filter(user=request.user, status="complete")
        serializer = VehicleRepairRequestSerializer(repair_requests, many=True)
        return Response(serializer.data)
    
    
    @action(detail=False, methods=['GET'])
    def user_active_repair_requests(self, request):
        repair_requests = VehicleRepairRequest.objects.filter(user=request.user).exclude(status="complete")
        serializer = VehicleRepairRequestSerializer(repair_requests, many=True)
        return Response(serializer.data)



class VehicleRepairRequestImageViewSet(BaseAPIMixin, ModelViewSet):
    queryset = VehicleRepairRequestImage.objects.all()
    serializer_class = VehicleRepairRequestImageSerializer

    def get_queryset(self):
        repair_request: VehicleRepairRequest = VehicleRepairRequest.objects.get(
            idx=self.kwargs["repair_request_idx"],
        )
        return VehicleRepairRequestImage.objects.filter(repair_request_id=repair_request.id)

    def get_serializer_context(self):
        return {"repair_request": self.kwargs["repair_request_idx"]}


class VehicleRepairRequestVideoViewSet(BaseAPIMixin, ModelViewSet):

    queryset = VehicleRepairRequestVideo.objects.all()
    serializer_class = VehicleRepairRequestVideoSerializer

    def get_queryset(self):
        repair_request: VehicleRepairRequest = VehicleRepairRequest.objects.get(
            idx=self.kwargs["repair_request_idx"],
        )
        return VehicleRepairRequestVideo.objects.filter(repair_request_id=repair_request.id)
