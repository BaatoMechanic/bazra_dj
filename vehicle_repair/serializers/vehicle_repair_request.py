from typing import Any, Dict, List

from django.contrib.auth import get_user_model

from rest_framework import serializers

from utils.mixins.serializer_field_mixins import DetailRelatedField
from utils.mixins.serializer_model_mixins import BaseModelSerializerMixin
from utils.tasks import send_bulk_notifications, send_notification
from vehicle_repair.models import (
    VehicleRepairRequest,
    VehicleRepairRequestImage,
    VehicleRepairRequestVideo,
)

User = get_user_model()


class VehicleRepairRequestSerializer(BaseModelSerializerMixin):
    user = DetailRelatedField(representation="user.idx")
    advance_charge = serializers.SerializerMethodField()
    display_image = serializers.SerializerMethodField()
    contact_number = DetailRelatedField(representation="user.phone")

    class Meta:
        model = VehicleRepairRequest
        fields = [
            "idx",
            "title",
            "description",
            "user",
            "vehicle_category",
            "service",
            "preferred_mechanic",
            "assigned_mechanic",
            "location",
            "status",
            "advance_payment_status",
            "advance_charge",
            "service_charge",
            "created_at",
            "display_image",
            "contact_number",
        ]

    def validate_location(self, value):
        if not value:
            raise serializers.ValidationError("Location is required.")
        return value

    def get_advance_charge(self, obj):
        # using method to return advance charge to fix couldn't serialize decimal object error
        return float(obj.advance_charge) if obj.advance_charge else None

    def get_display_image(self, obj) -> str | None:
        image = obj.images.first()
        if not image:
            return None
        return image.image.url

    def create(self, validated_data):
        user = self.context.get("request").user
        validated_data["user"] = user
        user_mobile_number = user.phone
        if not user_mobile_number:
            raise serializers.ValidationError({"detail": "User mobile number is required."})
        instance = super().create(validated_data)
        send_bulk_notifications.delay(
            list(User.objects.filter(primary_role__name="Mechanic").values_list("id", flat=True)),
            "New vehicle repair request",
            "There is a new vehicle repair request, you might like",
        )
        send_notification.delay(
            user.id,
            "Repair request sent successfully",
            "Your vehicle repair request has been sent. You'll be notified sortly",
        )
        return instance

    def update(self, instance, validated_data):
        assigned_mechanic = validated_data.get("assigned_mechanic")
        if assigned_mechanic and assigned_mechanic.is_engaged_in_repair():
            raise serializers.ValidationError(
                {
                    "detail": "Cannot work on multiple repair requests at the same"
                    "time. Please complete the previous repair first."
                }
            )
        return super().update(instance, validated_data)


class VehicleRepairRequestImageSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField(), required=False, write_only=True)
    image = serializers.ImageField(required=False)

    class Meta:
        model = VehicleRepairRequestImage
        fields = ["idx", "image", "images"]

    def create(self, validated_data: Dict[str, Any]) -> List[VehicleRepairRequestImage]:
        """
        Create VehicleRepairRequestImage objects with the given validated data.

        Args:
            validated_data (Dict[str, Any]): The validated data.

        Returns:
            List[VehicleRepairRequestImage]: The created VehicleRepairRequestImage objects.
        """
        images: List[VehicleRepairRequestImage] = []

        if "image" in validated_data:
            image = VehicleRepairRequestImage(
                repair_request=validated_data["repair_request"],
                image=validated_data["image"],
            )
            images.append(image)

        images.extend(
            [
                VehicleRepairRequestImage(repair_request=validated_data["repair_request"], image=image)
                for image in validated_data["images"]
            ]
        )

        return VehicleRepairRequestImage.objects.bulk_create(images)

    def save(self, **kwargs):
        if not self.validated_data.get("image") and not self.validated_data.get("images"):
            raise serializers.ValidationError({"detail": "At least one image is required."})

        repair_request_idx = self.context.get("repair_request")
        try:
            kwargs["repair_request"] = VehicleRepairRequest.objects.get(idx=repair_request_idx)
            return super().save(**kwargs)
        except VehicleRepairRequest.DoesNotExist:
            raise serializers.ValidationError({"detail": "Repair request does not exist."})


class VehicleRepairRequestVideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = VehicleRepairRequestVideo
        fields = ["idx", "video"]

    def save(self, **kwargs):
        repair_request_idx = self.context.get("repair_request")
        try:
            kwargs["repair_request"] = VehicleRepairRequest.objects.get(idx=repair_request_idx)
            return super().save(**kwargs)
        except VehicleRepairRequest.DoesNotExist:
            raise serializers.ValidationError({"detail": "Repair request does not exist."})
