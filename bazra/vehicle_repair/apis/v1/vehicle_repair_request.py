import json
from typing import Any, Dict

from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from utils.api_response import api_response_success
from utils.app_helpers.gis import send_request
from utils.mixins.api_mixins import BaseAPIMixin
from vehicle_repair.models import VehicleRepairRequest
from vehicle_repair.models.mechanic import Mechanic
from vehicle_repair.models.vehicle_repair_request import (
    VEHICLE_REPAIR_STATUS_CANCELLED,
    VEHICLE_REPAIR_STATUS_COMPLETE,
    VEHICLE_REPAIR_STATUS_PENDING,
    VEHICLE_REPAIR_STATUS_WAITING_COMPLETION_ACCEPTANCE,
    VehicleRepairRequestImage,
    VehicleRepairRequestVideo,
)
from vehicle_repair.serializers.service import ServiceSerializer
from vehicle_repair.serializers.vehicle_repair_request import (
    VehicleRepairRequestImageSerializer,
    VehicleRepairRequestSerializer,
    VehicleRepairRequestVideoSerializer,
)


class VehicleRepairRequestViewSet(BaseAPIMixin, ModelViewSet):

    queryset = VehicleRepairRequest.objects.all()
    serializer_class = VehicleRepairRequestSerializer

    def get_queryset(self):
        if self.action == "list":
            return (
                VehicleRepairRequest.objects.prefetch_related("images")
                .select_related("user")
                .filter(
                    (
                        ~Q(status=VEHICLE_REPAIR_STATUS_WAITING_COMPLETION_ACCEPTANCE)
                        & ~Q(status=VEHICLE_REPAIR_STATUS_COMPLETE)
                        & ~Q(status=VEHICLE_REPAIR_STATUS_CANCELLED)
                    ),
                    is_obsolete=False,
                )
                .order_by("-created_at")
            )

        return super().get_queryset()

    def get_serializer_context(self) -> Dict[str, Any]:
        return {"request": self.request}

    @action(detail=True, methods=["GET"])
    def service_type(self, request, idx):
        repair_request = get_object_or_404(VehicleRepairRequest, idx=idx)
        serializer = ServiceSerializer(repair_request.service)
        return Response(serializer.data)

    @action(detail=True, methods=["GET"])
    def user_repair_requests(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(user=request.user)
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=["GET"])
    def user_recent_repair_requests(self, request):
        repair_requests = VehicleRepairRequest.objects.filter(user=request.user, status="complete")
        serializer = VehicleRepairRequestSerializer(repair_requests, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def user_active_repair_requests(self, request):
        repair_requests = (
            VehicleRepairRequest.objects.filter(user=request.user).exclude(status="complete").order_by("-created_at")
        )
        serializer = VehicleRepairRequestSerializer(repair_requests, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["POST"])
    def advance_payment(self, request, idx):
        repair_request = get_object_or_404(VehicleRepairRequest, idx=idx)
        # repair_request.advance_payment = request.data["advance_payment"]
        mechanic_location = request.data["mechanic_location"]
        if isinstance(mechanic_location, str):
            mechanic_location = json.loads(mechanic_location)
        repair_location = repair_request.location
        url = (
            "http://maarga-container:5000/table/v1/driving/"
            f"{mechanic_location['longitude']},{mechanic_location['latitude']};"
            f"{repair_location['longitude']},{repair_location['latitude']}"
            "?sources=0&destinations=1&annotations=duration,distance"
        )
        response = send_request(url)
        data = json.loads(response.content)
        distance = data["distances"][0][0]
        lunch_charge = 0

        # add lunch charge if distance is more than 50km
        if distance > 50000:
            lunch_charge = 500

        # Charge will be 5 rupee per 1000 meter
        repair_request.advance_charge = round((distance / 1000) * 5 + lunch_charge, 2)

        repair_request.save(update_fields=["advance_charge"])
        serializer = VehicleRepairRequestSerializer(repair_request)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def mechanic_active_repair(self, request):
        mechanic = get_object_or_404(Mechanic, user=request.user)

        repair_request = (
            VehicleRepairRequest.objects.filter(
                assigned_mechanic=mechanic,
            )
            .exclude(Q(status=VEHICLE_REPAIR_STATUS_PENDING) | Q(status=VEHICLE_REPAIR_STATUS_COMPLETE))
            .last()
        )

        if not repair_request:
            return api_response_success({"detail": "No active repair request found"})
        serializer = VehicleRepairRequestSerializer(repair_request)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def mechanic_all_repairs(self, request):
        mechanic = get_object_or_404(Mechanic, user=request.user)

        repair_requests = VehicleRepairRequest.objects.filter(
            assigned_mechanic=mechanic, status=VEHICLE_REPAIR_STATUS_COMPLETE
        )
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

    def get_serializer_context(self):
        return {"repair_request": self.kwargs["repair_request_idx"]}
