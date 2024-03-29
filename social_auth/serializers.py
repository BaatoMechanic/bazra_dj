import os

from typing import Any, Optional

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from social_auth.register import register_social_user
from social_auth import google


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token: str) -> dict[str, Any]:
        """
        Validates a Google auth token and registers a new user or updates an existing user's info.

        Args:
            auth_token (str): The Google social auth token.

        Raises:
            serializers.ValidationError: If the token is invalid or expired.
            AuthenticationFailed: If the token's client ID cannot be confirmed.

        Returns:
            User: The registered or updated user.
        """
        user_data: dict[str, str] = google.Google.validate(auth_token)

        user_id: Optional[str] = user_data.pop("sub", None)
        if not user_id:
            raise serializers.ValidationError(
                "Invalid or expired token, please login again"
            )

        aud: str = user_data.pop("aud")
        if aud != os.environ.get("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY"):
            raise AuthenticationFailed(
                "Couldn't confirm who you are, please try again later"
            )

        return register_social_user(user_id=user_id, provider="google", **user_data)
