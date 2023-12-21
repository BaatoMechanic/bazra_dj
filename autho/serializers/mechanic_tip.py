import string
from typing import Any, Dict

from rest_framework import serializers


from autho.models import User
from autho.models.mechanic_tip import MechanicTip

from autho.models.rating_review import RatingAndReview
from autho.serializers.user_info import SimpleUserSerializer
from utils.mixins.serializer_mixins import BaseModelSerializerMixin


class MechanicTipSerializer(BaseModelSerializerMixin):
    mechanic = SimpleUserSerializer()

    class Meta:
        model = MechanicTip
        fields = ['idx', 'tip', 'mechanic']
