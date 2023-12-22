from rest_framework import serializers
from utils.helpers import check_identifier_is_email

from utils.serializer_fields import PasswordField, UserIdentifierField

from autho.models import User


class UserRegistrationSerializer(serializers.Serializer):
    user_identifier = UserIdentifierField()
    password = PasswordField()
    name = serializers.CharField()

    def create(self, validated_data):
        user_identifier = validated_data.pop('user_identifier')
        if not user_identifier:
            raise ValueError("Either or both of 'email and phone' is required to create a user.")

        user = User.get_user_by_identifier(user_identifier)
        if user is not None:
            raise ValueError("User already registered.")

        is_identifier_email = check_identifier_is_email(user_identifier)

        if is_identifier_email:
            validated_data['email'] = user_identifier
            validated_data.pop('phone', None)  # Remove phone field if present
        else:
            validated_data['phone'] = user_identifier
            validated_data.pop('email', None)  # Remove email field if present

        user = User.objects.create_user(**validated_data)
        return {
            "message": "User registered successfully."
        }
