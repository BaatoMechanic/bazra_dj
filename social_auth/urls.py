from django.urls import path
from . import views


urlpatterns = [
    path("google/", views.GoogleSocialAuthViewSet.as_view(), name="social_auth-google"),
]
