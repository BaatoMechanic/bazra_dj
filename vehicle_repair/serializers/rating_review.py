
from utils.mixins.serializer_model_mixins import BaseModelSerializerMixin
from vehicle_repair.models.rating_review import RatingAndReview


class RatingAndReviewSerializer(BaseModelSerializerMixin):

    class Meta:
        model = RatingAndReview
        fields = ["idx", "rating", "review", "review_by", "user"]
