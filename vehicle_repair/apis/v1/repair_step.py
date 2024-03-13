
from rest_framework.viewsets import ModelViewSet

from utils.mixins.base_api_mixin import BaseAPIMixin
from vehicle_repair.models import RepairStep
from vehicle_repair.serializers.repair_step import CreateRepairStepSerializer, RepairStepSerializer

# Create your views here.


class RepairStepViewSet(BaseAPIMixin, ModelViewSet):

    queryset = RepairStep.objects.all()
    serializer_class = RepairStepSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateRepairStepSerializer
        return super().get_serializer_class()
