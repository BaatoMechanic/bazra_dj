from django.db import models
from django.http import HttpRequest

from utils.mixins.base_model_mixin import BaseModelMixin
from utils.storage import PrivateMediaStorage


REPAIR_STEP_STATUS_PENDING = "pending"
REPAIR_STEP_STATUS_IN_PROGRESS = "in_progress"
REPAIR_STEP_STATUS_COMPLETE = "complete"
REPAIR_STEP_STATUS_CANCELLED = "cancelled"

REPAIR_STEP_STATUS_CHOICES = [
    (REPAIR_STEP_STATUS_PENDING, REPAIR_STEP_STATUS_PENDING.capitalize()),
    (REPAIR_STEP_STATUS_IN_PROGRESS, REPAIR_STEP_STATUS_IN_PROGRESS.capitalize()),
    (REPAIR_STEP_STATUS_COMPLETE, REPAIR_STEP_STATUS_COMPLETE.capitalize()),
    (REPAIR_STEP_STATUS_CANCELLED, REPAIR_STEP_STATUS_CANCELLED.capitalize()),
]


class RepairStep(BaseModelMixin):
    repair_request = models.ForeignKey(
        "vehicle_repair.VehicleRepairRequest", on_delete=models.CASCADE, related_name="repair_steps"
    )
    name = models.CharField(max_length=255)
    text_description = models.CharField(max_length=500, null=True, blank=True)
    audio_description = models.FileField(upload_to="repair_steps", null=True, blank=True)
    status = models.CharField(max_length=50, choices=REPAIR_STEP_STATUS_CHOICES, default=REPAIR_STEP_STATUS_PENDING)

    def __str__(self) -> str:
        return self.name

    def can_retrieve(self, request: HttpRequest) -> bool:
        if request.user.is_superuser:
            return True

        if request.user == self.repair_request.user:
            return True

        if request.user.isa("Mechanic"):
            return request.user.mechanic_profile == self.repair_request.assigned_mechanic

        return False

    def can_partial_update(self, request: HttpRequest) -> bool:
        return self.can_retrieve(request)


class RepairStepReport(BaseModelMixin):
    repair_step = models.OneToOneField(RepairStep, on_delete=models.PROTECT, related_name="report")

    def __str__(self) -> str:
        return self.repair_step.name


class RepairStepBillImage(BaseModelMixin):
    report = models.ForeignKey(RepairStepReport, on_delete=models.PROTECT, related_name="bill_images")
    image = models.ImageField(upload_to="repair_steps/bill_images", storage=PrivateMediaStorage())

    def __str__(self) -> str:
        return self.idx
