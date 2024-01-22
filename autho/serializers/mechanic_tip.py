from autho.models import MechanicTip
from autho.serializers import SimpleUserSerializer
from utils.mixins.serializer_mixins import BaseModelSerializerMixin


class MechanicTipSerializer(BaseModelSerializerMixin):
    mechanic = SimpleUserSerializer()

    class Meta:
        model = MechanicTip
        fields = ['idx', 'tip', 'mechanic']
