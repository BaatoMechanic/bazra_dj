from typing import Any, Dict, List

from django.contrib.auth import get_user_model

from rest_framework import serializers

from utils.mixins.serializer_mixins import BaseModelSerializerMixin
from vehicle_repair.models import (
    VehicleRepairRequest,
    Service,
    VehicleCategory,
    VehicleRepairRequestImage,
    VehicleRepairRequestVideo)
from vehicle_repair.models.mechanic import Mechanic

User = get_user_model()


class VehicleRepairRequestSerializer(BaseModelSerializerMixin):
    user = serializers.ReadOnlyField(source="user.idx")
    vehicle_type = serializers.CharField(source="vehicle_type.idx")
    # vehicle_part = serializers.CharField(source="vehicle_part.idx")
    service_type = serializers.CharField(source="service_type.idx")
    preferred_mechanic = serializers.CharField(source="preferred_mechanic.idx", required=False, allow_null=True)

    assigned_mechanic = serializers.CharField(source="assigned_mechanic.idx", required=False)

    class Meta:
        model = VehicleRepairRequest
        fields = ["idx", "title", "description", "user", "vehicle_type",
                  "service_type", "preferred_mechanic", "assigned_mechanic", "location", "status", "advance_payment_status", "created_at"]

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        user = self.context.get('request').user
        attrs["user"] = user

        vehicle_idx = attrs.pop("vehicle_type", {}).get('idx')
        if vehicle_idx:
            vehicle_type = VehicleCategory.objects.filter(idx=vehicle_idx).first()
            if not vehicle_type:
                raise serializers.ValidationError({"details": ["Vehicle type does not exist."]})
            attrs["vehicle_type"] = vehicle_type

        # vehicle_part_idx = attrs.pop("vehicle_part", {}).get('idx')
        # if vehicle_part_idx:
        #     vehicle_part = VehiclePart.objects.filter(idx=vehicle_part_idx).first()
        #     if not vehicle_part:
        #         raise serializers.ValidationError({"details": ["Vehicle part does not exist."]})
        #     attrs["vehicle_part"] = vehicle_part

        service_idx = attrs.pop("service_type", {}).get('idx')
        if service_idx:
            service = Service.objects.filter(idx=service_idx).first()
            if not service:
                raise serializers.ValidationError({"details": ["Service type does not exist."]})
            attrs["service_type"] = service

        preferred_mehanic_idx = attrs.pop("preferred_mechanic", {}).get('idx')
        if preferred_mehanic_idx:
            preferred_mehanic = User.objects.filter(idx=preferred_mehanic_idx).first()
            if not preferred_mehanic:
                raise serializers.ValidationError({"details": ["Preferred mechanic does not exist."]})
            if not hasattr(preferred_mehanic, "mechanic_profile"):
                raise serializers.ValidationError({"details": ["Invalid preferred mechanic."]})
            attrs['preferred_mechanic'] = preferred_mehanic

        return super().validate(attrs)

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        assigned_mechanic_idx = validated_data.pop('assigned_mechanic', None)
        if assigned_mechanic_idx:
            assigned_mechanic = Mechanic.objects.filter(idx=assigned_mechanic_idx).first()
            if not assigned_mechanic:
                raise serializers.ValidationError({"details": ["Mechanic does not exist."]})
            # if not hasattr(assigned_mechanic, "mechanic_profile"):
            #     raise serializers.ValidationError({"details": ["Not a mechanic user."]})
            validated_data['assigned_mechanic'] = assigned_mechanic

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
                image=validated_data["image"]
            )
            images.append(image)

        images.extend([
            VehicleRepairRequestImage(
                repair_request=validated_data["repair_request"],
                image=image
            ) for image in validated_data['images']
        ])

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
