from rest_framework.viewsets import ModelViewSet

from utils.mixins.api_mixins import BaseAPIMixin
from vehicle_repair.models import RepairStep
from vehicle_repair.models.repair_step import RepairStepReport
from vehicle_repair.serializers.repair_step import (
    CreateRepairStepReportSerializer,
    RepairStepReportSerializer,
    RepairStepSerializer,
)


class RepairStepViewSet(BaseAPIMixin, ModelViewSet):

    queryset = RepairStep.objects.all().order_by("created_at")
    serializer_class = RepairStepSerializer

    def get_serializer_context(self):
        return {"repair_request_idx": self.kwargs["repair_request_idx"]}

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(repair_request__idx=self.kwargs["repair_request_idx"])
        return super().list(request, *args, **kwargs)


class RepairStepReportViewSet(BaseAPIMixin, ModelViewSet):
    queryset = RepairStepReport.objects.all().order_by("created_at")
    serializer_class = RepairStepReportSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateRepairStepReportSerializer
        return super().get_serializer_class()

    def get_serializer_context(self):
        return {
            "repair_request_idx": self.kwargs["repair_request_idx"],
            "repair_step_idx": self.kwargs["repair_step_idx"],
        }
