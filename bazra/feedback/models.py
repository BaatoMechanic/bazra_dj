from django.db import models

from utils.mixins.base_model_mixin import BaseModelMixin
from django.conf import settings


class Feedback(BaseModelMixin):
    subject = models.CharField(max_length=255)
    message = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.subject
