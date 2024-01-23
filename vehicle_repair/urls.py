
# from django.urls import path
from . import views

from rest_framework_nested import routers

router = routers.DefaultRouter()

router.register("repair_requests", views.VehicleRepairRequestViewSet, basename="repair_requests")
router.register("services", views.ServiceViewSet, basename="services")
router.register("vehicle-categories", views.VehicleCategoryViewSet, basename="vehicle-categories")

router.register("mechanics", views.MechanicViewSet, basename="mechanics")
router.register("customers", views.CustomerViewSet, basename="customers")


repair_request_router = routers.NestedDefaultRouter(router, "repair_requests", lookup="repair_request")
repair_request_router.register("images", views.VehicleRepairRequestImageViewSet, basename="repair_request-images")
repair_request_router.register("videos", views.VehicleRepairRequestVideoViewSet, basename="repair_request-videos")
repair_request_router.register("repair_steps", views.RepairStepViewSet, basename="repair_request-steps")

urlpatterns = [

]

urlpatterns += router.urls + repair_request_router.urls
