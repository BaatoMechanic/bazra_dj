from typing import Dict, Any

from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from autho.models import User
from autho.serializers import RatingAndReviewSerializer
from vehicle_repair.models import RatingAndReview
from utils.mixins.base_api_mixin import BaseAPIMixin


class RatingAndReviewViewSet(BaseAPIMixin, ModelViewSet):
    queryset = RatingAndReview.objects.all()
    serializer_class = RatingAndReviewSerializer

    def get_serializer_context(self) -> Dict[str, Any]:
        return {"request": self.request}

    @action(detail=False, methods=["GET"])
    def mechanic_reviews(self, request):
        mechanic_id = self.request.query_params.get("idx", None)
        mechanic = get_object_or_404(User, idx=mechanic_id)
        self.queryset = RatingAndReview.objects.filter(user=mechanic)
        self.serializer_class = RatingAndReviewSerializer

        return super().list(request)
