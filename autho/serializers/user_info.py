
from rest_framework import serializers

# from django.contrib.auth import get_user_model

# User = get_user_model()

from autho.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['idx', 'name', 'email', 'phone', 'image', 'primary_role', 'roles']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.primary_role is not None:
            representation['primary_role'] = instance.primary_role.name
        representation['roles'] = [role.name for role in instance.roles.all()]
        return representation


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['idx', 'name', 'email', 'phone']
