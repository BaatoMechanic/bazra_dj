
from django.urls import path
from . import views

from rest_framework_nested import routers

router = routers.DefaultRouter()

router.register("reviews", views.RatingAndReviewViewSet, basename="reviews")
router.register("user_info", views.UserInfoViewSet, basename="user_info")
router.register('users_management', views.UserManagementViewSet, basename='users_management')
router.register('mechanic_tips', views.MechanicTipViewSet, basename='mechanic_tips')


urlpatterns = [
    path('create-token/', views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh-token/', views.TokenRefreshView.as_view(), name='token_refresh'),
    path('verify-token/', views.TokenVerifyView.as_view(), name='token_verify'),
    # path('register/', views.register_user, name='register'),

]

urlpatterns += router.urls
