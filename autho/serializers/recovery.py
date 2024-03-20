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


class VerfiyOtpSerializer(serializers.Serializer):
    opt = serializers.CharField(max_length=6)
    new_password = serializers.CharField()

    def validate_otp(self, value):
        if value.isdigit() and len(value) != 6:
            raise serializers.ValidationError("Invalid OTP")
        return value

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters")
        return value
