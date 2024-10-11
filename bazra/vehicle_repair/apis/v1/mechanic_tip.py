from utils.mixins.api_mixins import BaseAPIMixin

from rest_framework.viewsets import ModelViewSet

from vehicle_repair.models import MechanicTip
from vehicle_repair.serializers import MechanicTipSerializer


class MechanicTipViewSet(BaseAPIMixin, ModelViewSet):
    queryset = MechanicTip.objects.all()
    serializer_class = MechanicTipSerializer
