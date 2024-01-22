from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from autho.models import User
from utils.mixins.base_model_mixin import BaseModelMixin
from vehicle_repair.models import VehicleRepairRequest


class RatingAndReview(BaseModelMixin):
    rating = models.FloatField(validators=[
        MinValueValidator(1), MaxValueValidator(
            5)
    ])
    review = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rating_and_reviews")
    review_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="reviewed_by")
    repair_request = models.ForeignKey(VehicleRepairRequest,
                                       on_delete=models.SET_NULL, null=True,
                                       related_name="review_and_ratings")
