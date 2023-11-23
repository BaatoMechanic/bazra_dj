from django.db import models

from utils.mixins.base_model_mixin import BaseModelMixin

from django.contrib.auth import get_user_model
from vehicle_repair.models.vehicle_category import VehicleCategory

from vehicle_repair.models.vehicle_part import VehiclePart
User = get_user_model()


VEHICLE_REPAIR_STATUS_PENDING = "pending"
VEHICLE_REPAIR_STATUS_WAITING_FRO_USER_ACCEPTANCE = "waiting_for_user_acceptance"
VEHICLE_REPAIR_STATUS_WAITING_FRO_ADVANCE_PAYMENT = "waiting_for_advance_payment"
VEHICLE_REPAIR_STATUS_WAITING_FRO_MECHANIC = "waiting_for_mechanic"
VEHICLE_REPAIR_STATUS_IN_PROGRESS = "in_progress"
VEHICLE_REPAIR_STATUS_IN_HALT = "halt"
VEHICLE_REPAIR_STATUS_WAITING_COMPLETION_ACCEPTANCE = "waiting_for_completion_acceptance"
VEHICLE_REPAIR_STATUS_COMPLETED = "completed"
VEHICLE_REPAIR_STATUS_CANCELLED = "cancelled"


class VehicleRepairRequest(BaseModelMixin):

    customer = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="vehicle_repair_requests"
    )
    preferred_mechanic = models.OneToOneField(
        User, on_delete=models.SET_NULL, related_name="vehicle_repair_preferred_mechanics", null=True
    )
    assigned_mechanic = models.OneToOneField(
        User, on_delete=models.PROTECT, related_name="vehicle_repair_assigned_mechanics", null=True
    )
    vehicle_type = models.ForeignKey(VehicleCategory, on_delete=models.PROTECT, related_name="vehicle_repair")
    vehicle_part = models.ForeignKey(VehiclePart, on_delete=models.PROTECT, related_name="vehicle_repair")
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=255)
