from typing import Dict, Any

from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from utils.api_response import api_response_success
from vehicle_repair.models import RatingAndReview
from utils.mixins.api_mixins import BaseAPIMixin
from vehicle_repair.models.mechanic import Mechanic
from vehicle_repair.serializers.rating_review import VehicleRepairReviewSerializer


class RatingAndReviewViewSet(BaseAPIMixin, ModelViewSet):
    queryset = RatingAndReview.objects.all()
    serializer_class = VehicleRepairReviewSerializer

    def get_serializer_context(self) -> Dict[str, Any]:
        return {"request": self.request}

    @action(detail=False, methods=["GET"])
    def mechanic_reviews(self, request):
        mechanic_idx = self.request.query_params.get("idx", None)

        mechanic = get_object_or_404(Mechanic, idx=mechanic_idx)
        self.queryset = self.queryset.filter(user=mechanic.user.id)
        serializer = VehicleRepairReviewSerializer(self.queryset, many=True)
        return api_response_success(serializer.data)
