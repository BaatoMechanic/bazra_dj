from utils.mixins.base_model_mixin import BaseModelMixin

from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class UserLocation(BaseModelMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.FloatField()
    timestamp = models.DateTimeField()
    accuracy = models.FloatField()
    heading = models.FloatField()
    speed = models.FloatField()
    speed_accuracy = models.FloatField()
    location_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.latitude}, {self.longitude}"
