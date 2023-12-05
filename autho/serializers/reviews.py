from typing import Any, Dict

from rest_framework import serializers


from autho.models import User

from autho.models.rating_review import RatingAndReview
from utils.mixins.serializer_mixins import BaseModelSerializerMixin


class RatingAndReviewSerializer(BaseModelSerializerMixin):
    class Meta:
        model = RatingAndReview
        fields = ['rating', 'review', 'user', 'review_by']

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates the attributes.

        Args:
            attrs (dict): The attributes to validate.

        Returns:
            dict: The validated attributes.

        Raises:
            serializers.ValidationError: If the user is rating themselves.
        """
        review_by: User = self.context.get('request').user
        attrs['review_by'] = review_by

        user: User = attrs.get("user")

        if review_by == user:
            raise serializers.ValidationError({"user": ["You can't rate yourself."]})

        return super().validate(attrs)
