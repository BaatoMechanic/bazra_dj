# from autho.serializers import SimpleUserSerializer
from utils.mixins.serializer_model_mixins import BaseModelSerializerMixin
from vehicle_repair.models.mechanic_tip import MechanicTip
from .mechanic import MechanicSerializer


class MechanicTipSerializer(BaseModelSerializerMixin):
    # mechanic = SimpleUserSerializer()
    mechanic = MechanicSerializer()

    class Meta:
        model = MechanicTip
        fields = ["idx", "tip", "mechanic"]
