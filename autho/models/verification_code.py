
from django.utils import timezone
from django.db import models
from utils.helpers import generate_6digit_number


from django.conf import settings

from utils.mixins.base_model_mixin import BaseModelMixin


class VerificationCode(BaseModelMixin):
    user = models.OneToOneField(
        "autho.User", on_delete=models.CASCADE, related_name="verification_code")
    code = models.CharField(max_length=6, default=generate_6digit_number())
    created_on = models.DateTimeField(auto_now_add=True)
    tries = models.PositiveIntegerField(default=0)
    expires_on = models.DateTimeField(default=timezone.now() + timezone.timedelta(minutes=settings.OTP_TTL))

    def update_code(self):
        self.code = generate_6digit_number()
        self.tries = 0
        self.expires_on = timezone.now() + timezone.timedelta(minutes=settings.OTP_TTL)
        self.save()
        return self
