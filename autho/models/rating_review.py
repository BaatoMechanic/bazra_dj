
from django.db import models
from autho.models.user import User

from utils.mixins.base_model_mixin import BaseModelMixin


class RatingAndReview(BaseModelMixin):
    rating = models.IntegerField()
    review = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rating_and_reviews")
    review_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="reviewed_by")
