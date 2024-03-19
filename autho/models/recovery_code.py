import logging

from datetime import timezone

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from autho.exceptions import RecoveryCodeLockedException
from utils.mixins.base_exception_mixin import BMException
from utils.mixins.base_model_mixin import BaseModelMixin

User = get_user_model()
logger = logging.getLogger(__name__)


class RecoveryCode(BaseModelMixin):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recovery_code"
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
        if self.sents > self.max_sends:
            self.mark_inactive()
        self.save(update_fields=["sents", "is_active"])

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

        if self.phone:
            self.sms_code()
        elif self.email:
            self.email_code()
        else:
            raise BMException("User does not have phone or email")  # type: ignore

    def sms_code(self):
        pass

    def email_code(self):
        from django.core.mail import send_mail

        subject = "Autho Recovery Code"
        message = f"Your Autho Recovery Code is: {self.code}"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [self.email]

        send_mail(subject, message, from_email, recipient_list)
