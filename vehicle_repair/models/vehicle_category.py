

from django.db import models

from utils.mixins.base_model_mixin import BaseModelMixin


class VehicleCategory(BaseModelMixin):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to="vehicle_categories", null=True, blank=True)
