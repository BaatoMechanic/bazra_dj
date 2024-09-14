from typing import Any, Dict

from django.contrib.auth.models import update_last_login

from rest_framework import serializers

from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib import auth

from utils.tasks import send_notification


class LoginSerializer(serializers.Serializer):
    """
    This serializer overrides the TokenObtainPairSerializer of simple jwt to use custom field
    user_identifier and password to create the access and refresh token
    """

    user_identifier = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs: Dict[str, Any]) -> Dict[Any, Any]:
        data = super().validate(attrs)
        user_identifier = data.get("user_identifier")
        password = data.get("password")

        user = auth.authenticate(
            self.context.get("request"),
            user_identifier=user_identifier,
            password=password,
        )

        refresh = RefreshToken.for_user(user)

        update_last_login(None, user)
        # update_last_login.delay(None, user)
        # TODO: send sms about the login
        send_notification.delay(
            user, "New Login", "New login has been detected", image=user.image.url if user.image else None
        )

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
