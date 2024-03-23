import logging

from django.db import models
from django.utils import timezone

from utils.mixins.base_model_mixin import BaseModelMixin

logger = logging.getLogger(__name__)


class BaseOTPCode(BaseModelMixin):

    code = models.CharField(max_length=6)
    token = models.CharField(max_length=64, null=True)
    expired_on = models.DateTimeField(null=True)
    locked_at = models.DateTimeField(null=True)
    retries = models.PositiveSmallIntegerField(default=0)
    sents = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def lock(self):

        self.update(locked_at=timezone.now())

    def mark_inactive(self) -> None:
        """
        Marks the otp code instance as inactive.

        Args:
            None

        Returns:
            None
        """
        self.update(is_active=False)

    def mark_active(self) -> None:
        """
        Marks the otp code instance as active.

        Args:
            None

        Returns:
            None
        """
        self.update(is_active=True)

    def increment_retries(self) -> None:
        raise NotImplementedError()

    def increment_sents(self) -> None:
        raise NotImplementedError()
