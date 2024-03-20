from rest_framework import serializers

from autho.authentication import CustomSimpleJWTAuthentication


class SendRecoveryCodeSerializer(serializers.Serializer):
    user_identifier = serializers.CharField()

    def validate_user_identifier(self, value):
        banckend = CustomSimpleJWTAuthentication()
        user = banckend.get_user_from_identifier(value)
        if user is None:
            raise serializers.ValidationError("User not found")
        return user
