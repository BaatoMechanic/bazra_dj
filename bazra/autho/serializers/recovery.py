from rest_framework import serializers

from autho.authentication import CustomSimpleJWTAuthentication
from utils.helpers import is_valid_email


class SendRecoveryCodeSerializer(serializers.Serializer):
    user_identifier = serializers.CharField()

    def validate_user_identifier(self, value):
        banckend = CustomSimpleJWTAuthentication()
        user = banckend.get_user_from_identifier(value)
        if user is None:
            raise serializers.ValidationError("User not found")
        return user


class VerfiyRecoveryOtpSerializer(serializers.Serializer):
    new_password = serializers.CharField()

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters")
        return value


class VerifyOtpSerializer(serializers.Serializer):
    for_account_verification = serializers.BooleanField(default=False)
    user_identifier = serializers.CharField()
    # otp_code is optional because this serialization is also used during otp generation and
    # otp code is not available during otp generation
    otp_code = serializers.CharField(required=False)

    def validate_otp_code(self, value):
        if len(value) != 6:
            raise serializers.ValidationError("Invalid otp code")
        return value

    def validate_user_identifier(self, value):
        banckend = CustomSimpleJWTAuthentication()
        user = banckend.get_user_from_identifier(value)
        if user:
            is_email = is_valid_email(value)
            if is_email and user.is_email_verified:
                raise serializers.ValidationError("Email already verified")
            if not is_email and user.is_phone_verified:
                raise serializers.ValidationError("Phone already verified")
        # if user is None then it might be the account verification process
        return value
