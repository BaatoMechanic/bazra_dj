
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from autho.models.rating_review import RatingAndReview

from permission.permissions import BazraPermission

from rest_framework.viewsets import ModelViewSet

from utils.mixins.base_api_mixin import BaseAPIMixin


class TokenObtainPairView(TokenObtainPairView):
    permission_classes = ([BazraPermission])


class TokenRefreshView(TokenRefreshView):
    permission_classes = ([BazraPermission])


class TokenVerifyView(TokenVerifyView):
    permission_classes = ([BazraPermission])


class RatingAndReviewViewSet(BaseAPIMixin, ModelViewSet):
    serializer_class = None
    queryset = RatingAndReview.objects.all()
