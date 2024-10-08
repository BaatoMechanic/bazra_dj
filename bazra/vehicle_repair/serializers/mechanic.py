from rest_framework import serializers
from utils.mixins.serializer_field_mixins import DetailRelatedField
from utils.mixins.serializer_model_mixins import BaseModelSerializerMixin
from vehicle_repair.models import Mechanic


class MechanicSerializer(BaseModelSerializerMixin):
    name = DetailRelatedField(representation="user.name")
    dob_type = DetailRelatedField(representation="user.dob_type")
    dob = DetailRelatedField(representation="user.dob")
    additional_attributes = DetailRelatedField(representation="get_additional_attributes", is_method=True)
    roles = DetailRelatedField(representation="get_roles", is_method=True, source="user")
    # image = DetailRelatedField(representation="user.image.url")
    image = serializers.SerializerMethodField()

    class Meta:
        model = Mechanic
        fields = [
            "idx",
            "name",
            "vehicle_speciality",
            "service_speciality",
            "description",
            "dob_type",
            "dob",
            "roles",
            "image",
            "occupied",
            "additional_attributes",
        ]

    def get_image(self, obj):
        if obj.user.image:
            return obj.user.image.url
        return None
