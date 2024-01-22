

import json
from math import exp

from django.http import HttpResponse
from autho.models.location import UserLocation
from vehicle_repair.models.mechanic import Mechanic
from autho.serializers import UserSerializer
from autho.models import User

from rest_framework.decorators import action

from rest_framework.response import Response
from autho.serializers.location import UserLocationSerializer

from utils.mixins.base_api_mixin import BaseAPIMixin

from rest_framework.viewsets import ModelViewSet
from vehicle_repair.models.service import Service

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
    def location(self, request):
        # print(request.user)
        # user_idx = request.data.get('idxx')
        try:
            location = UserLocation.objects.filter(user=request.user).order_by('-created_at').first()
            serializer = UserLocationSerializer(location)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(status=404, data={'details': "User does not exist"})
