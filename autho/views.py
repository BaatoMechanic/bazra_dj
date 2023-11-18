
from rest_framework_simplejwt.views import TokenObtainPairView

from permission.permissions import BazraPermission


class TokenObtainPairView(TokenObtainPairView):
    permission_classes = ([BazraPermission])
