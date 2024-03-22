from typing import Any, Dict

from rest_framework import serializers

from vehicle_repair.models import RatingAndReview
from utils.mixins.serializer_model_mixins import BaseModelSerializerMixin
from vehicle_repair.models import VehicleRepairRequest
from django.contrib.contenttypes.models import ContentType

from vehicle_repair.models.mechanic import Mechanic


class VehicleRepairReviewSerializer(BaseModelSerializerMixin):
    reviewer = serializers.CharField(source="review_by", read_only=True)
    reviewed = serializers.CharField(source="user", read_only=True)
    repair_request_idx = serializers.CharField(write_only=True)
    repair_request = serializers.SerializerMethodField()

    mechanic = serializers.CharField(write_only=True)

    class Meta:
        model = RatingAndReview
        fields = [
            "idx",
            "rating",
            "review",
            "reviewer",
            "reviewed",
            "mechanic",
            "repair_request",
            "repair_request_idx",
            "created_at",
        ]

    def get_repair_request(self, obj):
        return obj.content_object.idx

    def create(self, validated_data):
        reviewer = self.context.get("request").user
        mechanic = validated_data.pop("mechanic")
        repair_request = validated_data.pop("repair_request", None)

        # Check if the user has already reviewed the repair request
        type = ContentType.objects.get_for_model(VehicleRepairRequest)

        if RatingAndReview.objects.filter(
            review_by=reviewer,
            user=mechanic.user,
            content_type=type,
            object_id=repair_request.id,
        ).exists():
            raise serializers.ValidationError(
                {"details": ["You have already reviewed this repair request."]}
            )

        validated_data["content_object"] = repair_request
        validated_data["user"] = mechanic.user

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

        review_by = self.context.get("request").user
        attrs["review_by"] = review_by

        mechanic_idx = attrs.get("mechanic")
        try:
            mechanic = Mechanic.objects.get(idx=mechanic_idx)
        except Mechanic.DoesNotExist:
            raise serializers.ValidationError(
                {"mechanic": ["Mechanic does not exist."]}
            )

        if review_by == mechanic.user:
            raise serializers.ValidationError({"user": ["You can't rate yourself."]})

        repair_request_idx = attrs.pop("repair_request_idx", None)
        if not repair_request_idx:
            raise serializers.ValidationError(
                {"details": ["Repair request must be provided."]}
            )

        repair_request = VehicleRepairRequest.objects.filter(
            idx=repair_request_idx
        ).first()
        if not repair_request:
            raise serializers.ValidationError(
                {"repair_request": ["Repair request does not exist."]}
            )
        attrs["repair_request"] = repair_request

        attrs["mechanic"] = mechanic

        return super().validate(attrs)
