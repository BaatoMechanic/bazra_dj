
from typing import Dict, Any
from autho.models.rating_review import RatingAndReview
from autho.serializers import RatingAndReviewSerializer

from utils.mixins.base_api_mixin import BaseAPIMixin

from rest_framework.viewsets import ModelViewSet


class RatingAndReviewViewSet(BaseAPIMixin, ModelViewSet):
    queryset = RatingAndReview.objects.all()
    serializer_class = RatingAndReviewSerializer


def get_serializer_context(self) -> Dict[str, Any]:
    return {"request": self.request}
