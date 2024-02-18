from rest_framework import serializers

from utils.mixins.serializer_mixins import BaseModelSerializerMixin
from vehicle_repair.models import Customer

from django.contrib.auth import get_user_model

User = get_user_model()


class CustomerSerializer(BaseModelSerializerMixin):
    user_idx = serializers.CharField(write_only=True)
    name = serializers.ReadOnlyField(source="user.name")
    email = serializers.ReadOnlyField(source="user.email")
    phone = serializers.ReadOnlyField(source="user.phone")
    dob_type = serializers.ReadOnlyField(source="user.dob_type")
    dob = serializers.ReadOnlyField(source="user.dob")
    primary_role = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()
    additional_attributes = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = fields = ['user_idx', 'idx', 'name', 'email', 'phone', "dob_type",
                           "dob", "primary_role", "roles", "additional_attributes"]

    def create(self, validated_data):
        user_idx = validated_data.pop('user_idx')
        user = User.objects.get(idx=user_idx)
        return Customer.objects.create(user=user, **validated_data)

    def get_primary_role(self, obj):
        if obj.user.primary_role:
            obj.user.primary_role.name
        return None

    def get_roles(self, obj):
        return [role.name for role in obj.user.roles.all()]

    def get_additional_attributes(self, obj):
        return {
            "is_phone_verified": obj.user.is_phone_verified,
            "is_email_verified": obj.user.is_email_verified,
            "is_verified": obj.user.is_verified
        }
