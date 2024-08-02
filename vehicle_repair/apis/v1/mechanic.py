from django.shortcuts import get_object_or_404
from rest_framework.decorators import action

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from utils.mixins.base_api_mixin import BaseAPIMixin
from vehicle_repair.models.mechanic import Mechanic
from vehicle_repair.models.service import Service
from vehicle_repair.models.vehicle_category import VehicleCategory
from vehicle_repair.serializers import MechanicSerializer

# Create your views here.


class MechanicViewSet(BaseAPIMixin, ModelViewSet):

    queryset = Mechanic.objects.all()
    serializer_class = MechanicSerializer

    @action(detail=False, methods=["GET"])
    def recommended_mechanics(self, request):
        vehicle_speciality_idx = request.query_params.get(
            "vehicle_category_speciality", None
        )
        service_speciality_idx = request.query_params.get("service_speciality", None)

        vehicle_speciality = None
        if vehicle_speciality_idx:
            vehicle_speciality = VehicleCategory.objects.filter(
                idx=vehicle_speciality_idx
            ).first()

        service_speciality = None
        if service_speciality_idx:
            service_speciality = Service.objects.filter(
                idx=service_speciality_idx
            ).first()

        mechanics = Mechanic.objects.filter(
            vehicle_speciality=vehicle_speciality, service_speciality=service_speciality
        ).select_related("user")

        serializer = MechanicSerializer(mechanics, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def me(self, request):
        mechanic = get_object_or_404(Mechanic, user=request.user)
        serializer = self.get_serializer(mechanic)
        return Response(serializer.data)
