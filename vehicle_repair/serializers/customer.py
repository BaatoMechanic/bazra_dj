from rest_framework import serializers
from utils.mixins.serializer_field_mixins import DetailRelatedField
from utils.mixins.serializer_model_mixins import BaseModelSerializerMixin
from vehicle_repair.models import Customer

from django.contrib.auth import get_user_model

User = get_user_model()


class CustomerSerializer(BaseModelSerializerMixin):
    user_idx = serializers.CharField(write_only=True)
    name = DetailRelatedField(representation="user.name")
    email = DetailRelatedField(representation="user.email")
    phone = DetailRelatedField(representation="user.phone")
    dob_type = DetailRelatedField(representation="user.dob_type")
    auth_provider = DetailRelatedField(representation="user.auth_provider")
    dob = DetailRelatedField(representation="user.dob")
    gender = DetailRelatedField(representation="user.gender")
    is_verified = DetailRelatedField(representation="user.is_verified")
    is_email_verified = DetailRelatedField(representation="user.is_email_verified")
    is_phone_verified = DetailRelatedField(representation="user.is_phone_verified")
    image = DetailRelatedField(representation="user.get_image_url")
    primary_role = serializers.SerializerMethodField()
    roles = DetailRelatedField(representation="get_roles", is_method=True, source="user")
    additional_attributes = DetailRelatedField(representation="get_additional_attributes", is_method=True)

    class Meta:
        model = Customer
        fields = [
            "user_idx",
            "idx",
            "name",
            "email",
            "phone",
            "dob_type",
            "dob",
            "gender",
            "primary_role",
            "auth_provider",
            "image",
            "is_verified",
            "is_email_verified",
            "is_phone_verified",
            "roles",
            "additional_attributes",
        ]

    def create(self, validated_data):
        user_idx = validated_data.pop("user_idx")
        user = User.objects.get(idx=user_idx)
        return Customer.objects.create(user=user, **validated_data)

    def get_primary_role(self, obj):
        if obj.user.primary_role:
            return obj.user.primary_role.name.lower()
        return None
