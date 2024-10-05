import os

from typing import Any, Dict, Union, cast

from google.auth.transport import requests
from google.oauth2 import id_token


class Google:
    @staticmethod
    def validate(auth_token: str) -> Union[Dict[str, Any], str]:
        """
        Validates the given authentication token for Google OAuth2.

        Args:
            auth_token (str): The authentication token to be validated.

        Returns:
            Union[Dict[str, Any], str]: If the token is valid, returns a dictionary containing
                                            the verified ID token information.
                                        If the token is expired or invalid, returns the string
                                            "Token either expired or invalid".
        """

        try:
            idinfo: Dict[str, Any] = id_token.verify_oauth2_token(
                auth_token,
                requests.Request(),
                cast(str, os.environ.get("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")),
            )

            if "accounts.google.com" in idinfo.get("iss", ""):
                return idinfo

        except Exception:
            return "Token either expired or invalid"
