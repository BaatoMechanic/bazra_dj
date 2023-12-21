

import json
from math import exp

from django.http import HttpResponse
from autho.models.location import UserLocation
from autho.models.mechanic_profile import MechanicProfile
from autho.serializers import UserSerializer
from autho.models import User

from rest_framework.decorators import action

from rest_framework.response import Response
from autho.serializers.location import UserLocationSerializer

from utils.mixins.base_api_mixin import BaseAPIMixin

from rest_framework.viewsets import ModelViewSet

from vehicle_repair.models.vehicle_category import VehicleCategory
from vehicle_repair.models.vehicle_part import VehiclePart


class UserInfoViewSet(BaseAPIMixin, ModelViewSet):
    '''
    This file is responsible to perform all the user info logic for the project.
    Any user information logic should be added here.
    '''

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        user = User.objects.get(
            id=request.user.id)
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = UserSerializer(user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def recommended_mechanics(self, request):
        vehicle_speciality_idx = request.data.get('vehicle_category', None)
        part_speciality_idx = request.data.get('vehicle_part', None)

        vehicle_speciality = None
        if vehicle_speciality_idx:
            vehicle_speciality = VehicleCategory.objects.filter(idx=vehicle_speciality_idx).first()

        part_speciality = None
        if part_speciality_idx:
            part_speciality = VehiclePart.objects.filter(idx=part_speciality_idx).first()

        profiles = MechanicProfile.objects.filter(
            vehicle_speciality=vehicle_speciality,
            vehicle_part_speciality=part_speciality
        ).select_related('mechanic')

        mechanics = [profile.mechanic for profile in profiles]

        serializer = UserSerializer(mechanics, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def location(self, request):
        user_idx = request.data.get('idxx')
        try:
            user = User.objects.get(idx=user_idx)
            location = UserLocation.objects.filter(user=user).last()
            serializer = UserLocationSerializer(location)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(status=404, data={'detail': "User does not exist"})
