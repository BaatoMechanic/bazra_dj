from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from social_auth.register import register_social_user

from social_auth import google


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)

        try:

            user_data["sub"]
        except KeyError:
            raise serializers.ValidationError(
                "Invalid or expired token, please login again"
            )

        # if(user_data['email_verified'] == False):
        #     raise serializers.ValidationError(
        #         'Email not verified, please verify your email and try again')

        if user_data["aud"] != settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY:
            raise AuthenticationFailed(
                "Couldn't confirm who you are, please try again later"
            )

        user_id = user_data["sub"]
        email = user_data["email"]
        name = user_data["name"]
        picture = user_data["picture"]
        provider = "google"

        # return register_social_user(user_id=user_id, email=email, name=name, picture=picture, provider=provider)
        return register_social_user(
            user_id=user_id, email=email, name=name, provider=provider, picture=picture
        )
