from typing import Any, Dict
from rest_framework import serializers
from utils.helpers import is_valid_email

from utils.serializer_fields import UserIdentifierField

from autho.models import User


class UserRegistrationSerializer(serializers.Serializer):
    user_identifier = UserIdentifierField()
    name = serializers.CharField()
    gender = serializers.ChoiceField(choices=User.GENDER_CHOCES)

    def create(self, validated_data: Dict[str, Any]) -> User:
        user_identifier = validated_data.pop("user_identifier")
        if not user_identifier:
            raise ValueError("Either or both of 'email and phone' is required to create a user.")

        user = User.get_user_by_identifier(user_identifier)
        if user:
            raise ValueError("User already registered.")

        is_identifier_email = is_valid_email(user_identifier)

        if is_identifier_email:
            validated_data["email"] = user_identifier
            validated_data.pop("phone", None)  # Remove phone field if present
        else:
            validated_data["phone"] = user_identifier
            validated_data.pop("email", None)  # Remove email field if present

        return User.objects.create_user(set_unusable_password=True, **validated_data)
