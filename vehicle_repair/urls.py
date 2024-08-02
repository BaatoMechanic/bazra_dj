# from django.urls import path
from .apis import v1

from rest_framework_nested import routers

router = routers.DefaultRouter()

router.register("repair_requests", v1.VehicleRepairRequestViewSet, basename="repair_requests")
router.register("services", v1.ServiceViewSet, basename="services")
router.register("vehicle-categories", v1.VehicleCategoryViewSet, basename="vehicle-categories")
router.register("mechanic_tips", v1.MechanicTipViewSet, basename="mechanic_tips")
router.register("reviews", v1.RatingAndReviewViewSet, basename="reviews")

router.register("mechanics", v1.MechanicViewSet, basename="mechanics")
router.register("customers", v1.CustomerViewSet, basename="customers")


repair_request_router = routers.NestedDefaultRouter(router, "repair_requests", lookup="repair_request")
repair_request_router.register("images", v1.VehicleRepairRequestImageViewSet, basename="repair_request-images")
repair_request_router.register("videos", v1.VehicleRepairRequestVideoViewSet, basename="repair_request-videos")
repair_request_router.register("repair_steps", v1.RepairStepViewSet, basename="repair_request-steps")

report_step_router = routers.NestedDefaultRouter(repair_request_router, "repair_steps", lookup="repair_step")
report_step_router.register("reports", v1.RepairStepReportViewSet, basename="repair_step-reports")

urlpatterns = []

urlpatterns += router.urls + repair_request_router.urls + report_step_router.urls
