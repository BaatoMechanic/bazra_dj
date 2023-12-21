
from django.db import models

from utils.mixins.base_model_mixin import BaseModelMixin
from vehicle_repair.models.vehicle_category import VehicleCategory


class VehiclePart(BaseModelMixin):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    vehicle_type = models.ForeignKey(VehicleCategory, on_delete=models.PROTECT, related_name="vehicle_parts")
    image = models.ImageField(upload_to="vehicle_parts", null=True, blank=True)
    is_multiple = models.BooleanField(default=False)
    position = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name
