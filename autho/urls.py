
from django.urls import path
from . import views

from rest_framework_nested import routers

router = routers.DefaultRouter()

router.register("reviews", views.RatingAndReviewViewSet, basename="reviews")

urlpatterns = [
    path('create-token/', views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh-token/', views.TokenRefreshView.as_view(), name='token_refresh'),
    path('verify-token/', views.TokenVerifyView.as_view(), name='token_verify'),
]

urlpatterns += router.urls
