from rest_framework import serializers

# from django.contrib.auth import get_user_model

# User = get_user_model()

from autho.models import User


class UserSerializer(serializers.ModelSerializer):
    roles = serializers.ReadOnlyField()
    primary_role = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = [
            "idx",
            "name",
            "email",
            "phone",
            "gender",
            "dob_type",
            "image",
            "primary_role",
            "roles",
            "auth_provider",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.primary_role is not None:
            representation["primary_role"] = instance.primary_role.name.lower()
        representation["roles"] = [role.name.lower() for role in instance.roles.all()]

        return representation


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["idx", "name", "image"]
