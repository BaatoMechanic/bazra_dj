from typing import Any, Dict

from rest_framework import serializers

from autho.models import User
from vehicle_repair.models import RatingAndReview
from utils.mixins.serializer_mixins import BaseModelSerializerMixin
from vehicle_repair.models import VehicleRepairRequest


class RatingAndReviewSerializer(BaseModelSerializerMixin):
    reviewer = serializers.CharField(source='review_by', read_only=True)
    reviewed = serializers.CharField(source='user', read_only=True)
    repair_request = serializers.CharField(required=False)
    user = serializers.CharField(write_only=True)

    class Meta:
        model = RatingAndReview
        fields = ['idx', 'rating', 'review', 'reviewer', 'reviewed', 'user', "repair_request", 'created_at']

    def create(self, validated_data):
        reviewer = self.context.get('request').user
        user_idx = validated_data.pop('user')
        try:
            user = User.objects.get(idx=user_idx)
            validated_data['review_by'] = reviewer
            validated_data['user'] = user
        except User.DoesNotExist:
            raise serializers.ValidationError({"details": ["User does not exist."]})

        if reviewer == user:
            raise serializers.ValidationError({"details": ["You can't review yourself."]})

        repair_request_idx = validated_data.pop('repair_request', None)

        if repair_request_idx:
            repair_request = VehicleRepairRequest.objects.filter(idx=repair_request_idx).first()
            if not repair_request:
                raise serializers.ValidationError({"details": ["Repair request does not exist."]})

            validated_data['repair_request'] = repair_request

        # Check if the user has already reviewed the repair request
        if RatingAndReview.objects.filter(review_by=reviewer, user=user, repair_request=repair_request).exists():
            raise serializers.ValidationError({"details": ["You have already reviewed this repair request."]})

        return super().create(validated_data)

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

        review_by = self.context.get('request').user
        attrs['review_by'] = review_by

        user_idx = attrs.get("user")
        try:
            user = User.objects.get(idx=user_idx)
        except User.DoesNotExist:
            raise serializers.ValidationError({"user": ["User does not exist."]})

        if review_by == user:
            raise serializers.ValidationError({"user": ["You can't rate yourself."]})

        repair_request_idx = attrs.pop("repair_request", None)
        if repair_request_idx:
            repair_request = VehicleRepairRequest.objects.filter(idx=repair_request_idx).first()
            if not repair_request:
                raise serializers.ValidationError({"repair_request": ["Repair request does not exist."]})
            attrs['repair_request'] = repair_request

        attrs['user'] = user

        return super().validate(attrs)
