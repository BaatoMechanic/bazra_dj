
# from django.urls import path
from . import views

from rest_framework_nested import routers

router = routers.DefaultRouter()

router.register("repair_requests", views.VehicleRepairRequestViewSet, basename="repair_requests")

repair_request_router = routers.NestedDefaultRouter(router, "repair_requests", lookup="repair_request")
repair_request_router.register("images", views.VehicleRepairRequestImageViewSet, basename="repair_request-images")
repair_request_router.register("videos", views.VehicleRepairRequestVideoViewSet, basename="repair_request-videos")

urlpatterns = [

]

urlpatterns += router.urls + repair_request_router.urls
