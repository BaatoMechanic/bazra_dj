# # from rest_framework.viewsets import ModelViewSet
# from rest_framework.viewsets import GenericViewSet
# from rest_framework.mixins import (
#     CreateModelMixin,
#     UpdateModelMixin,
#     RetrieveModelMixin,
#     DestroyModelMixin,
# )
# from utils.mixins.base_api_mixin import BaseAPIMixin
# from vehicle_repair.models import RatingAndReview, VehicleRepairRequest
# from vehicle_repair.serializers import RatingAndReviewSerializer


# class RatingAndReviewViewSet(BaseAPIMixin, ModelViewSet):
# class RatingAndReviewViewSet(
#     BaseAPIMixin,
#     RetrieveModelMixin,
#     CreateModelMixin,
#     UpdateModelMixin,
#     DestroyModelMixin,
#     GenericViewSet,
# ):
#     serializer_class = RatingAndReviewSerializer
#     queryset = RatingAndReview.objects.all()

#     # def get_queryset(self):

#     #     repair_request: VehicleRepairRequest = VehicleRepairRequest.objects.get(
#     #         idx=self.kwargs["repair_request_idx"],
#     #     )
#     #     return RatingAndReview.objects.filter(content_object=repair_request)


from typing import Dict, Any

from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from autho.models import User
from vehicle_repair.models import RatingAndReview
from utils.mixins.base_api_mixin import BaseAPIMixin
from vehicle_repair.serializers.rating_review import VehicleRepairReviewSerializer


class RatingAndReviewViewSet(BaseAPIMixin, ModelViewSet):
    queryset = RatingAndReview.objects.all()
    serializer_class = VehicleRepairReviewSerializer

    def get_serializer_context(self) -> Dict[str, Any]:
        return {"request": self.request}

    @action(detail=False, methods=["GET"])
    def mechanic_reviews(self, request):
        mechanic_id = self.request.query_params.get("idx", None)
        mechanic = get_object_or_404(User, idx=mechanic_id)
        self.queryset = RatingAndReview.objects.filter(user=mechanic)
        self.serializer_class = VehicleRepairReviewSerializer

        return super().list(request)
