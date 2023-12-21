
from utils.mixins.serializer_mixins import BaseModelSerializerMixin
from vehicle_repair.models.service import Service


class ServiceSerializer(BaseModelSerializerMixin):

    class Meta:
        model = Service
        fields = ["idx", "name", "description", "type", "image", "parts_included"]
