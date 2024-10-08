from django.db import models

from rest_framework.request import Request

from utils.mixins.base_model_mixin import BaseModelMixin


class VehicleCategory(BaseModelMixin):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to="vehicle_categories", null=True, blank=True)

    class Meta:
        verbose_name = "vehicle category"
        verbose_name_plural = "vehicle categories"

    def __str__(self) -> str:
        return self.name

    def can_retrieve(self, request: Request) -> bool:
        return True
