from rest_framework import serializers
from utils.mixins.serializer_field_mixins import BDetailRelatedField

from utils.mixins.serializer_model_mixins import BaseModelSerializerMixin
from vehicle_repair.models import Customer

from django.contrib.auth import get_user_model

User = get_user_model()


class CustomerSerializer(BaseModelSerializerMixin):
    user_idx = serializers.CharField(write_only=True)
    name = BDetailRelatedField(Customer, representation="user.name")
    email = BDetailRelatedField(Customer, representation="user.email")
    phone = BDetailRelatedField(Customer, representation="user.phone")
    dob_type = BDetailRelatedField(Customer, representation="user.dob_type")
    auth_provider = BDetailRelatedField(Customer, representation="user.auth_provider")
    dob = BDetailRelatedField(Customer, representation="user.dob")
    image = BDetailRelatedField(Customer, representation="user.get_image_url")
    primary_role = serializers.SerializerMethodField()
    roles = BDetailRelatedField(Customer, representation="get_roles", is_method=True, source="user")
    additional_attributes = BDetailRelatedField(Customer, representation="get_additional_attributes", is_method=True)

    class Meta:
        model = Customer
        fields = ['user_idx', 'idx', 'name', 'email', 'phone', "dob_type",
                  "dob", "primary_role", "auth_provider", "image", "roles", "additional_attributes"]

    def create(self, validated_data):
        user_idx = validated_data.pop('user_idx')
        user = User.objects.get(idx=user_idx)
        return Customer.objects.create(user=user, **validated_data)

    def get_primary_role(self, obj):
        if obj.user.primary_role:
            obj.user.primary_role.name
        return None
