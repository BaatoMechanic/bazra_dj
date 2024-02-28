from django.conf import settings
from django.db import models
from django.http import HttpRequest

from utils.mixins.base_model_mixin import BaseModelMixin


class Customer(BaseModelMixin):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name="customer_profile")

    def __str__(self) -> str:
        return f"Customer: {self.user.name}"

    def can_retrieve(self, request: HttpRequest) -> bool:
        # return request.user == self.user
        return True

    def get_additional_attributes(self) -> dict:
        return self.user.get_basic_attributes()
