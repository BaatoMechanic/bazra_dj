import string
from typing import Any, Dict

from rest_framework import serializers


from autho.models import User

from autho.models.rating_review import RatingAndReview
from utils.mixins.serializer_mixins import BaseModelSerializerMixin


class RatingAndReviewSerializer(BaseModelSerializerMixin):
    reviewer = serializers.CharField(source='review_by', read_only=True)
    reviewed = serializers.CharField(source='user', read_only=True)
    user = serializers.CharField(write_only=True)

    class Meta:
        model = RatingAndReview
        # fields = ['idx', 'rating', 'review', 'user', 'review_by']
        fields = ['idx', 'rating', 'review', 'reviewer', 'reviewed', 'user', 'created_at']

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

        userIdx: string = attrs.get("user")
        user: User = User.objects.get(idx=userIdx)

        if review_by == user:
            raise serializers.ValidationError({"user": ["You can't rate yourself."]})

        attrs['user'] = user
        return super().validate(attrs)
