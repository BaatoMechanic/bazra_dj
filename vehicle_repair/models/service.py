
from django.db import models

from utils.mixins.base_model_mixin import BaseModelMixin
from vehicle_repair.models.vehicle_part import VehiclePart


SERVICE_TYPE_OPTION_BODY_REPAIR = "body_repair"
SERVICE_TYPE_OPTION_ENGINE_REPAIR = "engine_repair"
SERVICE_TYPE_OPTION_ELECTRIC_REPAIR = "electric_repair"
SERVICE_TYPE_OPTION_WHEEL_REPAIR = "wheell_repair"
SERVICE_TYPE_OPTION_PAINTING = "painting"
SERVICE_TYPE_OPTION_OTHER = "other"

SERVICE_TYPE_OPTION_CHOICES = [
    (SERVICE_TYPE_OPTION_BODY_REPAIR, SERVICE_TYPE_OPTION_BODY_REPAIR.capitalize()),
    (SERVICE_TYPE_OPTION_ENGINE_REPAIR, SERVICE_TYPE_OPTION_ENGINE_REPAIR.capitalize()),
    (SERVICE_TYPE_OPTION_ELECTRIC_REPAIR, SERVICE_TYPE_OPTION_ELECTRIC_REPAIR.capitalize()),
    (SERVICE_TYPE_OPTION_WHEEL_REPAIR, SERVICE_TYPE_OPTION_WHEEL_REPAIR.capitalize()),
    (SERVICE_TYPE_OPTION_PAINTING, SERVICE_TYPE_OPTION_PAINTING.capitalize()),
    (SERVICE_TYPE_OPTION_OTHER, SERVICE_TYPE_OPTION_OTHER.capitalize()),
]


class Service(BaseModelMixin):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    parts_included = models.ManyToManyField(VehiclePart, related_name="services")
    type = models.CharField(max_length=50,
                            choices=SERVICE_TYPE_OPTION_CHOICES,
                            default=SERVICE_TYPE_OPTION_ENGINE_REPAIR)
    image = models.ImageField(upload_to="service/icons", null=True, blank=True)

    def __str__(self) -> str:
        return self.name
