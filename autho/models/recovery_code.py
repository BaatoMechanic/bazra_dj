import datetime
import logging

from django.conf import settings
from django.db import models
from django.utils import timezone

from autho.exceptions import RecoveryCodeLockedException
from utils.helpers import generate_6digit_number
from utils.mixins.base_exception_mixin import BMException
from utils.mixins.base_model_mixin import BaseModelMixin
from utils.tasks import send_email

logger = logging.getLogger(__name__)


class RecoveryCode(BaseModelMixin):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recovery_code"
    )
    code = models.CharField(max_length=6)
    expired_on = models.DateTimeField(null=True)
    locked_at = models.DateTimeField(null=True)
    retries = models.PositiveSmallIntegerField(default=0)
    sents = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def lock(self):
        self.update(locked_at=timezone.now())
        raise RecoveryCodeLockedException

    def mark_inactive(self) -> None:
        """
        Marks the RecoveryCode instance as inactive.

        Args:
            None

        Returns:
            None
        """
        self.update(is_active=False)

    def mark_active(self) -> None:
        """
        Marks the RecoveryCode instance as active.

        Args:
            None

        Returns:
            None
        """
        self.update(is_active=True)

    def increment_retries(self) -> None:
        """
        Increments the number of retries for the RecoveryCode instance and
        locks it if the maximum retries limit is reached.

        Args:
            None

        Returns:
            None
        """
        self.retries += 1
        if self.retries > settings.RECOVERY_CODE["MAX_RETRIES"]:
            self.lock()
        self.save(update_fields=["retries"])

    def increment_sents(self) -> None:
        """
        Increments the number of sends for the RecoveryCode instance and
        marks it as inactive if the maximum sends limit is reached.

        Args:
            None

        Returns:
            None
        """
        self.sents += 1
        if self.sents > settings.RECOVERY_CODE["MAX_SENDS"]:
            self.mark_inactive()
        self.save(update_fields=["sents", "is_active"])

    @classmethod
    def generate_recovery_code(cls, user) -> "RecoveryCode":
        recovery_code, _ = cls.objects.get_or_create(user=user)
        recovery_code.update_code()
        return recovery_code

    def update_code(self):
        self.code = generate_6digit_number()
        self.tries = 0
        self.sents = 0
        self.expired_on = timezone.now() + datetime.timedelta(
            minutes=settings.RECOVERY_CODE["OTP_TTL"]
        )
        self.save()
        return self

    def send(self) -> None:
        """
        Sends a recovery code to the user's phone or email.

        Args:
            None

        Returns:
            None
        """
        if settings.STAGING:
            logger.info(
                f"[Sending recovery code]: User Identifier: {self.user.phone}, code: {self.code}"
            )
            return self

        self.increment_sents()
        if self.sents > settings.RECOVERY_CODE["MAX_SENDS"]:
            self.mark_inactive()

        if not self.user.phone and not self.user.email:
            raise BMException("User does not have phone or email")
        if self.user.phone:
            self.sms_code()
        if self.user.email:
            self.email_code()

    def sms_code(self):
        pass

    def email_code(self):

        subject = "Password recovery code"
        message = f"Your password recovery code is: {self.code}"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [self.user.email]

        send_email(subject, message, recipient_list, from_email=from_email)
