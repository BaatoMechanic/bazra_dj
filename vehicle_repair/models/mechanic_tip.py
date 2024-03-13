from django.db import models

from utils.mixins.base_model_mixin import BaseModelMixin
from vehicle_repair.models.mechanic import Mechanic


class MechanicTip(BaseModelMixin):
    tip = models.CharField(max_length=500)
    mechanic = models.ForeignKey(
        Mechanic,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mechanic_tips",
    )
