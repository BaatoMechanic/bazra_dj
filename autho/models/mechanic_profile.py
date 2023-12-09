
from django.db import models

from utils.mixins.base_model_mixin import BaseModelMixin
from django.contrib.auth import get_user_model

User = get_user_model()


class MechanicProfile(BaseModelMixin):
    mechanic = models.OneToOneField(User, on_delete=models.CASCADE, related_name="mechanic_profile")
    vehicle_speciality = models.ForeignKey(
        "vehicle_repair.VehicleCategory", on_delete=models.SET_NULL, null=True)
    vehicle_part_speciality = models.ForeignKey(
        "vehicle_repair.VehiclePart", on_delete=models.SET_NULL, null=True
    )
    mechanic_description = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self) -> str:
        return f"Mechanic: {self.mechanic.name}"
