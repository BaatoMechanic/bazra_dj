


from typing import Dict, Any
from autho.models import MechanicTip
from autho.serializers import MechanicTipSerializer

from utils.mixins.base_api_mixin import BaseAPIMixin

from rest_framework.viewsets import ModelViewSet


class MechanicTipViewSet(BaseAPIMixin, ModelViewSet):
    queryset = MechanicTip.objects.all()
    serializer_class = MechanicTipSerializer

    