from django.urls import path
from .apis import v1

from rest_framework_nested import routers

router = routers.DefaultRouter()


router.register("user_info", v1.UserInfoViewSet, basename="user_info")
router.register(
    "users_management", v1.UserManagementViewSet, basename="users_management"
)
router.register(
    "account_recovery", v1.AccountRecoveryViewSet.as_view(), basename="account_recovery"
)


urlpatterns = [
    path("create-token/", v1.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh-token/", v1.TokenRefreshView.as_view(), name="token_refresh"),
    path("verify-token/", v1.TokenVerifyView.as_view(), name="token_verify"),
    # path('register/', views.register_user, name='register'),
]

urlpatterns += router.urls
