from rest_framework import serializers
from autho.serializers.user_info import UserSerializer

from utils.mixins.serializer_mixins import BaseModelSerializerMixin
from vehicle_repair.models import Customer


class CustomerSerializer(BaseModelSerializerMixin):
    name = serializers.ReadOnlyField(source="user.name")
    email = serializers.ReadOnlyField(source="user.email")
    phone = serializers.ReadOnlyField(source="user.phone")
    # image = serializers.ReadOnlyField(source="user.image")
    primary_role = serializers.ReadOnlyField(source="user.primary_role")
    roles = serializers.ReadOnlyField(source="user.roles")

    class Meta:
        model = Customer
        fields = fields = ['idx', 'name', 'email', 'phone',
                           'primary_role', 'roles']
