

import string
from typing import Any, Dict

from rest_framework import serializers


from autho.models import User
from autho.models.location import UserLocation
from autho.models.mechanic_tip import MechanicTip

from autho.models.rating_review import RatingAndReview
from autho.serializers.user_info import SimpleUserSerializer
from utils.mixins.serializer_mixins import BaseModelSerializerMixin


class UserLocationSerializer(BaseModelSerializerMixin):
    # mechanic = SimpleUserSerializer()

    class Meta:
        model = UserLocation
        fields = ['idx', 'latitude', 'longitude', 'altitude', 'timestamp',
                  'accuracy', 'heading', 'speed', 'speed_accuracy', 'location_name']

    def save(self, **kwargs):
        self.validated_data['user_id'] = kwargs.get('user').id
        return super().save(**kwargs)
