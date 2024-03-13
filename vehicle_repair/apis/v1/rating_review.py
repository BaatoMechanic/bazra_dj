from rest_framework.viewsets import ModelViewSet

from utils.mixins.base_api_mixin import BaseAPIMixin
from vehicle_repair.models import RatingAndReview, VehicleRepairRequest
from vehicle_repair.serializers import RatingAndReviewSerializer


class RatingAndReviewViewSet(BaseAPIMixin, ModelViewSet):
    serializer_class = RatingAndReviewSerializer

    def get_queryset(self):
        repair_request: VehicleRepairRequest = VehicleRepairRequest.objects.get(
            idx=self.kwargs["repair_request_idx"],
        )
        return RatingAndReview.objects.filter(content_object=repair_request)
