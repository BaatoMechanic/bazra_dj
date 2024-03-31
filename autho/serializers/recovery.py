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


class VerfiyRecoveryOtpCodeSerializer(serializers.Serializer):
    new_password = serializers.CharField()

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters")
        return value


class SendVerificationCodeSerializer(serializers.Serializer):
    user_identifier = serializers.CharField()

    def validate_user_identifier(self, value):
        banckend = CustomSimpleJWTAuthentication()
        user = banckend.get_user_from_identifier(value)
        if user is None:
            raise serializers.ValidationError("User not found")
        return user


class VerfiyVerificationOtpCodeSerializer(serializers.Serializer):
    new_password = serializers.CharField()

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters")
        return value
