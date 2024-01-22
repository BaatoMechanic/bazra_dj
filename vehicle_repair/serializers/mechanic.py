from rest_framework import serializers

from utils.mixins.serializer_mixins import BaseModelSerializerMixin
from vehicle_repair.models import Mechanic


class MechanicSerializer(BaseModelSerializerMixin):
    name = serializers.ReadOnlyField(source="user.name")

    class Meta:
        model = Mechanic
        fields = ["idx", "name", "vehicle_speciality", "service_speciality", "description"]
