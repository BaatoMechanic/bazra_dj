from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.http import HttpRequest

from autho.models import User
from utils.mixins.base_model_mixin import BaseModelMixin


class RatingAndReview(BaseModelMixin):
    rating = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="rating_and_reviews"
    )
    review_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="reviewed_by"
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    reviews = GenericRelation("RatingAndReview")

    def can_retrieve(self, request: HttpRequest) -> bool:
        return True
