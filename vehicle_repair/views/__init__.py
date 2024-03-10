from vehicle_repair.views.vehicle_category import VehicleCategoryViewSet
from .service import ServiceViewSet
from .vehicle_repair_request import (
    VehicleRepairRequestViewSet,
    VehicleRepairRequestImageViewSet,
    VehicleRepairRequestVideoViewSet,
)

from .repair_step import RepairStepViewSet
from .mechanic import MechanicViewSet
from .customer import CustomerViewSet
from .rating_review import RatingAndReviewViewSet