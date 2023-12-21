from tkinter import NO
from typing import Any, Dict
from django.forms import model_to_dict

from rest_framework import serializers
from utils.mixins.serializer_mixins import BaseModelSerializerMixin


from vehicle_repair.models import VehicleRepairRequest


from django.contrib.auth import get_user_model


from vehicle_repair.models.vehicle_category import VehicleCategory
from vehicle_repair.models.vehicle_part import VehiclePart
from vehicle_repair.models.vehicle_repair_request import VehicleRepairRequestImage, VehicleRepairRequestVideo

User = get_user_model()


class VehicleRepairRequestSerializer(BaseModelSerializerMixin):
    user = serializers.ReadOnlyField(source="user.idx")
    vehicle_type = serializers.CharField(source="vehicle_type.idx")
    vehicle_part = serializers.CharField(source="vehicle_part.idx")
    preferred_mechanic = serializers.CharField(source="preferred_mechanic.idx", required=False)

    assigned_mechanic = serializers.CharField(required=False)

    class Meta:
        model = VehicleRepairRequest
        fields = ["idx", "title", "description", "user", "vehicle_type",
                  "vehicle_part", "preferred_mechanic", "assigned_mechanic", "status"]

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        user = self.context.get('request').user
        attrs["user"] = user

        vehicle_idx = attrs.pop("vehicle_type", None)
        if vehicle_idx:
            vehicle_type = VehicleCategory.objects.filter(idx=vehicle_idx.get('idx')).first()
            if not vehicle_type:
                raise serializers.ValidationError({"detail": ["Vehicle type does not exist."]})
            attrs["vehicle_type"] = vehicle_type

        vehicle_part_idx = attrs.pop("vehicle_part", None)
        if vehicle_part_idx:
            vehicle_part = VehiclePart.objects.filter(idx=vehicle_part_idx.get('idx')).first()
            if not vehicle_part:
                raise serializers.ValidationError({"detail": ["Vehicle part does not exist."]})
            attrs["vehicle_part"] = vehicle_part

        preferred_mehanic_idx = attrs.pop("preferred_mechanic", None)
        if preferred_mehanic_idx:
            preferred_mehanic = User.objects.filter(idx=preferred_mehanic_idx.get('idx')).first()
            if not preferred_mehanic:
                raise serializers.ValidationError({"detail": ["Preferred mechanic does not exist."]})
            if not hasattr(preferred_mehanic, "mechanic_profile"):
                raise serializers.ValidationError({"detail": ["Invalid preferred mechanic."]})
            attrs['preferred_mechanic'] = preferred_mehanic

        return super().validate(attrs)

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        assigned_mechanic_idx = validated_data.pop('assigned_mechanic', None)
        if assigned_mechanic_idx:
            assigned_mechanic = User.objects.filter(idx=assigned_mechanic_idx).first()
            if not assigned_mechanic:
                raise serializers.ValidationError({"detail": ["Mechanic does not exist."]})
            if not hasattr(assigned_mechanic, "mechanic_profile"):
                raise serializers.ValidationError({"detail": ["Not a mechanic user."]})
            validated_data['assigned_mechanic'] = assigned_mechanic

        return super().update(instance, validated_data)


class VehicleRepairRequestImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = VehicleRepairRequestImage
        fields = ["idx", "image"]


class VehicleRepairRequestVideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = VehicleRepairRequestVideo
        fields = ["idx", "video"]
