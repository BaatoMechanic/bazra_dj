from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model

from vehicle_repair.models import Customer


def register_social_user(provider, user_id, email, name, picture):
    User = get_user_model()
    filtered_user_by_email = User.objects.filter(email=email)
    if filtered_user_by_email.exists():
        if provider == filtered_user_by_email[0].auth_provider:
            registered_user = authenticate(
                email=email, password=settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET
            )

            registered_customer = Customer.objects.get(user=registered_user)

            return {
                "phone": registered_user.phone,
                "email": registered_user.email,
                "first_name": registered_user.first_name,
                "last_name": registered_user.last_name,
                "picture": registered_customer.image.name,
                "tokens": registered_user.tokens(),
            }
        else:
            raise AuthenticationFailed(
                "Please continue your login using "
                + filtered_user_by_email[0].auth_provider
            )
    else:
        user = {
            "email": email,
            "password": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
        }
        user = User.objects.create_user(**user)
        # user.is_verified = True
        user.auth_provider = provider
        user.first_name = name.split(" ")[0]
        user.last_name = name.split(" ")[1]
        user.image = picture
        user.save()

        if user:
            customer = Customer.objects.create(user=user) # noqa

        new_user = authenticate(
            email=email, password=settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET
        )
        return {
            "username": new_user.username,
            "email": new_user.email,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "picture": picture,
            "tokens": new_user.tokens(),
        }
