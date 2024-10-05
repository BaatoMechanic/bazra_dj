from rest_framework_nested import routers

from .views import FeedbackViewSet

router = routers.DefaultRouter()


router.register("", FeedbackViewSet, basename="feedback")

urlpatterns = router.urls
