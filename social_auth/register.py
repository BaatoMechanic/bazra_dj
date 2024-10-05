from typing import Any

from django.contrib.auth import authenticate, get_user_model

from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, Token

from permission.models import Role
from vehicle_repair.models import Customer
from vehicle_repair.serializers import CustomerSerializer


def register_social_user(
    provider: str, user_id: str, email: str, name: str, picture: str, **kwargs: dict
) -> dict[str, Any]:
    """
    Register a social user.

    Args:
        provider (str): The provider of the user.
        user_id (str): The unique identifier of the user.
        email (str): The email of the user.
        name (str): The name of the user.
        picture (str): The picture of the user.
        **kwargs (dict): Additional keyword arguments.

    Returns:
        dict: A dictionary containing the user data and tokens.
    """
    User = get_user_model()

    try:
        user = User.objects.get(email=email, is_obsolete=False)
        if user.auth_provider != provider:
            raise AuthenticationFailed("Please continue your login using " + user.auth_provider)
    except User.DoesNotExist:
        user = User.objects.create_user(
            email=email,
            password=user_id,
            auth_provider=provider,
            name=name,
            primary_role=Role.objects.get(name="Consumer"),
            image=picture,
        )

    registered_user = authenticate(
        user_identifier=email,
        password=user_id,
    )

    refresh: Token = RefreshToken.for_user(registered_user)
    customer, _ = Customer.objects.get_or_create(user=user)
    serializer = CustomerSerializer(customer)

    # send_notification.delay(
    #     user.id, "New Login", "New login has been detected", image=user.image.url
    # )

    return {
        "user": serializer.data,
        "tokens": {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        },
    }
