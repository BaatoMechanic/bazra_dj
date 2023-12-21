
from django.db import models
from autho.models.user import User

from utils.mixins.base_model_mixin import BaseModelMixin


class MechanicTip(BaseModelMixin):
    tip = models.CharField(max_length=500)
    mechanic = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="mechanic_tips")
