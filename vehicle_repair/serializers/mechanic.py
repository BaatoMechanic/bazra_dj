from rest_framework import serializers
from utils.mixins.serializer_field_mixins import BDetailRelatedField

from utils.mixins.serializer_model_mixins import BaseModelSerializerMixin
from vehicle_repair.models import Mechanic


class MechanicSerializer(BaseModelSerializerMixin):
    name = BDetailRelatedField(Mechanic, representation="user.name")
    dob_type = BDetailRelatedField(Mechanic, representation="user.dob_type")
    dob = BDetailRelatedField(Mechanic, representation="user.dob")
    additional_attributes = serializers.SerializerMethodField()
    roles = BDetailRelatedField(
        Mechanic, representation="get_roles", is_method=True, source="user"
    )
    image = BDetailRelatedField(Mechanic, representation="user.image.url")

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

    def get_additional_attributes(self, obj):
        return {
            "is_phone_verified": obj.user.is_phone_verified,
            "is_email_verified": obj.user.is_email_verified,
            "is_verified": obj.user.is_verified,
            "total_repairs": obj.total_repairs,
            "total_reviews": obj.total_reviews,
        }
