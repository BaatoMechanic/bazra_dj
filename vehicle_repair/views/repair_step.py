
from rest_framework.viewsets import ModelViewSet

from utils.mixins.base_api_mixin import BaseAPIMixin
from vehicle_repair.models import RepairStep
from vehicle_repair.serializers.repair_step import RepairStepSerializer

# Create your views here.


class RepairStepViewSet(BaseAPIMixin, ModelViewSet):

    queryset = RepairStep.objects.all()
    serializer_class = RepairStepSerializer
