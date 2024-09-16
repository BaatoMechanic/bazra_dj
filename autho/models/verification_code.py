import datetime
from venv import logger
from django.http import HttpRequest
from django.utils import timezone
from django.db import models

from autho.exceptions import (
    InvalidVerificationCodeError,
    VerificationCodeLockedError,
)
from autho.models.base_models import BaseOTPCode
from utils.helpers import generate_6digit_number, generate_random_string


from django.conf import settings

from utils.mixins.base_exception_mixin import BMException
from utils.tasks import send_email, send_staging_email


def get_otp_expires_on():
    return timezone.now() + timezone.timedelta(minutes=settings.OTP_TTL)


class VerificationCode(BaseOTPCode):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="verification_code",
    )
    meta = models.JSONField(default=dict)

    def can_check_otp(self, request: HttpRequest):
        return True

    def can_resend(self, request: HttpRequest):
        return True

    def can_verify_otp(self, request: HttpRequest):
        return True

    def can_verify_account_otp(self, request: HttpRequest):
        return True

    def lock(self):
        super().lock()
        raise VerificationCodeLockedError

    def increment_retries(self) -> None:
        """
        Increments the number of retries for the Verification Code instance and
        locks it if the maximum retries limit is reached.

        Args:
            None

        Returns:
            None
        """
        self.retries += 1
        if self.retries > settings.VERIFICATION_CODE["MAX_RETRIES"]:
            self.save(update_fields=["retries"])
            self.lock()

    def increment_sents(self) -> None:
        """
        Increments the number of sends for the Verification Code instance and
        marks it as inactive if the maximum sends limit is reached.

        Args:
            None

        Returns:
            None
        """
        self.sents += 1
        if self.sents > settings.VERIFICATION_CODE["MAX_SENDS"]:
            self.mark_inactive()
            self.save(update_fields=["sents", "is_active"])

    @classmethod
    def generate_verification_code(cls, user) -> "VerificationCode":
        verification_code, _ = cls.objects.get_or_create(user=user)
        verification_code.update_code()
        return verification_code

    def update_code(self):
        self.code = generate_6digit_number()
        self.token = generate_random_string(64)
        self.tries = 0
        self.sents = 0
        self.expired_on = timezone.now() + datetime.timedelta(minutes=settings.VERIFICATION_CODE["OTP_TTL"])
        self.save()
        return self

    def equals(self, code, token=None):
        if not self.is_active:
            raise InvalidVerificationCodeError
        if settings.STAGING:
            return True
        if token:
            return self.code == code and self.token == token
        return self.code == code

    def send(self) -> None:
        """
        Sends a verification code to the user's phone or email.

        Args:
            None

        Returns:
            None
        """
        if settings.STAGING:
            logger.info(
                f"[Sending verification code]: "
                f"User Identifier: {self.user.phone if self.user.phone else self.user.email}, code: {self.code}"
            )

        self.increment_sents()
        if self.sents > settings.VERIFICATION_CODE["MAX_SENDS"]:
            self.mark_inactive()

        if not self.user.phone and not self.user.email:
            raise BMException("User does not have phone or email")
        if self.user.phone:
            self.sms_code()
        if self.user.email:
            self.email_code()

    def sms_code(self):
        if settings.STAGING:
            logger.info(f"[Skipping SMS]: Skipping sms being sent to {self.user.phone}")
            send_staging_email(
                "Verification Code SMS",
                f"Your account verification code is {self.code}",
            )

        # TODO:: Add SMS functionality here

    def email_code(self):
        subject = "Account verification code"
        message = f"Your account verification code is: {self.code}"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [self.user.email]
        template_name: str = "email/account_verification.html"
        context = {
            "user_name": self.user.name,
            # "recovery_link": f"http://localhost:8000/autho/account_recovery/
            # verify_otp_email/?token={self.token}&user={self.user.id}",
            "verification_code": self.code,
        }

        send_email(
            subject,
            message,
            recipient_list,
            from_email=from_email,
            template=template_name,
            template_context=context,
        )
