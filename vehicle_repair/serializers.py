from typing import Any, Dict
from django.forms import model_to_dict

from rest_framework import serializers
from utils.mixins.serializer_mixins import BaseModelSerializerMixin

from vehicle_repair.models import VehicleRepairRequest


from django.contrib.auth import get_user_model


from autho.serializers import SimpleUserSerializer
from vehicle_repair.models.vehicle_repair_request import VehicleRepairRequestImage, VehicleRepairRequestVideo

User = get_user_model()


class VehicleRepairRequestSerializer(BaseModelSerializerMixin):
    # user = serializers.ReadOnlyField(source="vehicle_repair_requests")
    # user = serializers.ReadOnlyField()
    user = SimpleUserSerializer(read_only=True)
    status = serializers.ReadOnlyField()
    assigned_mechanic = serializers.ReadOnlyField()

    class Meta:
        model = VehicleRepairRequest
        fields = ["idx", "title", "description", "user", "vehicle_type",
                  "vehicle_part", "preferred_mechanic", "assigned_mechanic", "status"]

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        user: User = self.context.get('request').user
        attrs["user"] = user

        preferred_mehanic = attrs.get("preferred_mechanic")

        if not hasattr(preferred_mehanic, "mechanic_profile"):
            raise serializers.ValidationError({"preferred_mechanic": ["Invalid mechanic."]})

        return super().validate(attrs)


class VehicleRepairRequestImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = VehicleRepairRequestImage
        fields = ["idx", "image"]


class VehicleRepairRequestVideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = VehicleRepairRequestVideo
        fields = ["idx", "video"]
