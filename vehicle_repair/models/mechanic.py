from django.db import models
from django.db.models import Q
from django.http import HttpRequest

from utils.mixins.base_model_mixin import BaseModelMixin

from django.conf import settings


class Mechanic(BaseModelMixin):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="mechanic_profile",
    )
    vehicle_speciality = models.ForeignKey("vehicle_repair.VehicleCategory", on_delete=models.SET_NULL, null=True)
    service_speciality = models.ForeignKey("vehicle_repair.Service", on_delete=models.SET_NULL, null=True)
    occupied = models.BooleanField(default=False)
    description = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self) -> str:
        return f"Mechanic: {self.user.name}"

    def can_retrieve(self, request: HttpRequest) -> bool:
        return True

    @property
    def total_repairs(self):
        from .vehicle_repair_request import VehicleRepairRequest

        return VehicleRepairRequest.objects.filter(assigned_mechanic=self).count()

    @property
    def total_reviews(self):
        from vehicle_repair.models.rating_review import RatingAndReview

        return RatingAndReview.objects.filter(user=self.user).count()

    def get_additional_attributes(self) -> dict:
        return {
            **self.user.get_basic_attributes(),
            "total_repairs": self.total_repairs,
            "total_reviews": self.total_reviews,
        }

    def is_engaged_in_repair(self) -> bool:
        from vehicle_repair.models.vehicle_repair_request import (
            VEHICLE_REPAIR_STATUS_CANCELLED,
            VEHICLE_REPAIR_STATUS_COMPLETE,
            VehicleRepairRequest,
        )

        return VehicleRepairRequest.objects.filter(
            (~Q(status=VEHICLE_REPAIR_STATUS_COMPLETE) & ~Q(status=VEHICLE_REPAIR_STATUS_CANCELLED)),
            assigned_mechanic=self,
        ).exists()
