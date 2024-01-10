
from django.db import models
from autho.models.rating_review import RatingAndReview

from utils.mixins.base_model_mixin import BaseModelMixin

from vehicle_repair.models import VehicleRepairRequest
from django.contrib.auth import get_user_model

User = get_user_model()


class MechanicProfile(BaseModelMixin):
    mechanic = models.OneToOneField(User, on_delete=models.CASCADE, related_name="mechanic_profile")
    vehicle_speciality = models.ForeignKey(
        "vehicle_repair.VehicleCategory", on_delete=models.SET_NULL, null=True)
    service_speciality = models.ForeignKey(
        "vehicle_repair.Service", on_delete=models.SET_NULL, null=True
    )
    mechanic_description = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self) -> str:
        return f"Mechanic: {self.mechanic.name}"

    @property
    def total_repairs(self):
        return VehicleRepairRequest.objects.filter(assigned_mechanic=self.mechanic).count()

    @property
    def total_reviews(self):
        return RatingAndReview.objects.filter(user=self.mechanic).count()
