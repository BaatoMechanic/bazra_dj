
from django.db import models

from utils.mixins.base_model_mixin import BaseModelMixin
from django.contrib.auth import get_user_model

User = get_user_model()


class MechanicAttribute(BaseModelMixin):
    mechanic = models.OneToOneField(User, on_delete=models.CASCADE, related_name="mechanic_attribute")
    vehicle_speciality = models.ForeignKey(
        "vehicle_repair.VehicleCategory", on_delete=models.SET_NULL, null=True)
    vehicle_part_speciality = models.ForeignKey(
        "vehicle_repair.VehiclePart", on_delete=models.SET_NULL, null=True
    )
