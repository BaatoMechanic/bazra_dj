
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


from permission.permissions import BazraPermission


# This file is responsible to perform all the authentication logic for the project.
# Any authentication logic should be added here.


class TokenObtainPairView(TokenObtainPairView):
    permission_classes = ([BazraPermission])


class TokenRefreshView(TokenRefreshView):
    permission_classes = ([BazraPermission])


class TokenVerifyView(TokenVerifyView):
    permission_classes = ([BazraPermission])


