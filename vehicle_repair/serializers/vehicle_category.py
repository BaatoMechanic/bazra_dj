from utils.mixins.serializer_mixins import BaseModelSerializerMixin
from vehicle_repair.models.vehicle_category import VehicleCategory


class VehicleCategorySerializer(BaseModelSerializerMixin):

    class Meta:
        model = VehicleCategory
        fields = ["idx", "name", "description", "image"]
