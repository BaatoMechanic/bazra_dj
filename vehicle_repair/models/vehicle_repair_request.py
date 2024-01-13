
from email.policy import default
from django.db import models


from django.http import HttpRequest
from utils.mixins.base_model_mixin import BaseModelMixin
from vehicle_repair.models.service import Service

from vehicle_repair.models.vehicle_category import VehicleCategory

from vehicle_repair.models.vehicle_part import VehiclePart

# from utils.validators import validate_file_size

from django.contrib.auth import get_user_model

User = get_user_model()


VEHICLE_REPAIR_STATUS_PENDING = "pending"
VEHICLE_REPAIR_STATUS_WAITING_FRO_USER_ACCEPTANCE = "waiting_for_user_acceptance"
VEHICLE_REPAIR_STATUS_WAITING_FRO_ADVANCE_PAYMENT = "waiting_for_advance_payment"
VEHICLE_REPAIR_STATUS_WAITING_FRO_MECHANIC = "waiting_for_mechanic"
VEHICLE_REPAIR_STATUS_IN_PROGRESS = "in_progress"
VEHICLE_REPAIR_STATUS_IN_HALT = "halt"
VEHICLE_REPAIR_STATUS_WAITING_COMPLETION_ACCEPTANCE = "waiting_for_completion_acceptance"
VEHICLE_REPAIR_STATUS_COMPLETED = "complete"
VEHICLE_REPAIR_STATUS_CANCELLED = "cancelled"


VEHICLE_REPAIR_STATUS_CHOICES = [
    (VEHICLE_REPAIR_STATUS_PENDING, VEHICLE_REPAIR_STATUS_PENDING.capitalize()),
    (VEHICLE_REPAIR_STATUS_WAITING_FRO_USER_ACCEPTANCE, VEHICLE_REPAIR_STATUS_WAITING_FRO_USER_ACCEPTANCE.capitalize()),
    (VEHICLE_REPAIR_STATUS_WAITING_FRO_ADVANCE_PAYMENT, VEHICLE_REPAIR_STATUS_WAITING_FRO_ADVANCE_PAYMENT.capitalize()),
    (VEHICLE_REPAIR_STATUS_WAITING_FRO_MECHANIC, VEHICLE_REPAIR_STATUS_WAITING_FRO_MECHANIC.capitalize()),
    (VEHICLE_REPAIR_STATUS_IN_PROGRESS, VEHICLE_REPAIR_STATUS_IN_PROGRESS.capitalize()),
    (VEHICLE_REPAIR_STATUS_IN_HALT, VEHICLE_REPAIR_STATUS_IN_HALT.capitalize()),
    (VEHICLE_REPAIR_STATUS_WAITING_COMPLETION_ACCEPTANCE, VEHICLE_REPAIR_STATUS_WAITING_COMPLETION_ACCEPTANCE.capitalize()),
    (VEHICLE_REPAIR_STATUS_COMPLETED, VEHICLE_REPAIR_STATUS_COMPLETED.capitalize()),
    (VEHICLE_REPAIR_STATUS_CANCELLED, VEHICLE_REPAIR_STATUS_CANCELLED.capitalize()),
]


class VehicleRepairRequest(BaseModelMixin):

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=255, default=VEHICLE_REPAIR_STATUS_PENDING,
                              choices=VEHICLE_REPAIR_STATUS_CHOICES)
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="vehicle_repair_requests"
    )
    preferred_mechanic = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="vehicle_repairs_preferred_mechanic", null=True
    )
    assigned_mechanic = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="vehicle_repairs_assigned_mechanic", null=True
    )
    vehicle_type = models.ForeignKey(VehicleCategory, on_delete=models.PROTECT, related_name="vehicle_repair")
    service_type = models.ForeignKey(Service, on_delete=models.PROTECT, related_name="vehicle_repair")
    # vehicle_part = models.ForeignKey(VehiclePart, on_delete=models.PROTECT, related_name="vehicle_repair")
    # lat, long, location_name and timestamp are most. Accuracy, altitude and other attributes are optional
    location = models.JSONField(default=dict)

    def __str__(self) -> str:
        # return f"{self.user} => {self.title}"
        return self.idx

    def can_retrieve(self, request: HttpRequest) -> bool:
        """
        Check if the current user can retrieve the data.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            bool: True if the user can retrieve the data, False otherwise.
        """
        request_user: User = request.user

        if request_user.isa("Superuser"):
            return True

        user: User = self.user
        assigned_mechanic: User = self.assigned_mechanic

        return request_user == user or request_user == assigned_mechanic

    def can_partial_update(self, request: HttpRequest) -> bool:
        request_user: User = request.user

        if request_user.isa("Superuser"):
            return True

        user: User = self.user

        return request_user == user

    def can_update(self, request: HttpRequest) -> bool:
        return True
        # request_user: User = request.user

        # if request_user.isa("Superuser"):
        #     return True

        # user: User = self.user

        # return request_user == user


class VehicleRepairRequestImage(BaseModelMixin):
    repair_request = models.ForeignKey(VehicleRepairRequest, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="vehicle_repair_request/images")
    # image = models.ImageField(upload_to="vehicle_repair_request/images", validators=[validate_file_size])

    def __str__(self) -> str:
        return self.idx

    def can_retrieve(self, request: HttpRequest) -> bool:
        return True

    def can_update(self, request: HttpRequest) -> bool:
        return True

    def can_partial_update(self, request: HttpRequest) -> bool:
        return True

    def can_destroy(self, request: HttpRequest) -> bool:
        request_user: User = request.user

        if request_user.isa("Superuser"):
            return True

        user: User = self.repair_request.user

        return request_user == user


class VehicleRepairRequestVideo(BaseModelMixin):
    repair_request = models.ForeignKey(VehicleRepairRequest, on_delete=models.CASCADE, related_name="videos")
    video = models.ImageField(upload_to="vehicle_repair_request/videos")

    def __str__(self) -> str:
        return self.idx

    def can_retrieve(self, request: HttpRequest) -> bool:
        return True
