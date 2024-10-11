from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from django.conf import settings
from rest_framework import status

from autho.exceptions import InvalidRecoveryCodeError, RecoveryCodeLockedError
from autho.models import User
from autho.models.recovery_code import RecoveryCode
from autho.serializers.recovery import (
    SendRecoveryCodeSerializer,
    VerfiyRecoveryOtpSerializer,
)
from utils.api_response import api_response_error, api_response_success
from utils.helpers import is_valid_mobile_number
from utils.mixins.api_mixins import BaseAPIMixin


class AccountRecoveryViewSet(BaseAPIMixin, GenericViewSet):
    queryset = RecoveryCode.objects.all()

    def get_serializer_class(self):
        if self.action == "send_otp_uid":
            return SendRecoveryCodeSerializer
        if self.action == "verify_otp":
            return VerfiyRecoveryOtpSerializer

    @action(detail=False, methods=["POST"])
    def send_otp_uid(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get("user_identifier")
        code: RecoveryCode = user.gen_recovery_code()
        id = request.data.get("user_identifier")
        code.send(id)

        return api_response_success(
            {
                "recovery": {
                    "idx": code.idx,
                },
                "message": (
                    f"Please check your " f"{'mobile' if is_valid_mobile_number(id) else 'email'} " f"for the otp code"
                ),
            }
        )

    @action(detail=False, methods=["POST"])
    def send_otp_password(self, request, *args, **kwargs):
        user: User = request.user
        is_correct = user.check_password(request.data.get("old_password"))
        if is_correct:
            code: RecoveryCode = user.gen_recovery_code()
            code.send()

            return api_response_success(
                {
                    "recovery": {
                        "idx": code.idx,
                    },
                    "message": "Please check your mobile and email for otp code ",
                }
            )
        else:
            return api_response_error(
                {"detail": "Old password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, methods=["POST"])
    def resend(self, request, *args, **kwargs):
        recovery_idx = request.data.get("idx")
        try:
            code = RecoveryCode.objects.get(idx=recovery_idx)

        except RecoveryCode.DoesNotExist:

            return api_response_success({"detail": "Resend the Otp again."})

        code.update_code()
        return api_response_success({"detail": "Resend sent successfully."})

    @action(detail=False, methods=["POST"])
    def check_otp(self, request, *args, **kwargs):
        if settings.STAGING:
            return api_response_success({"detail": "Valid otp"})
        code = RecoveryCode.objects.filter(idx=request.data.get("otp")).first()

        if code and code.code == request.data.get("code"):
            return api_response_success({"detail": "Valid otp"})

        return api_response_error({"detail": "Invalid otp"})

    @action(detail=True, methods=["POST"])
    def verify_otp(self, request, *args, **kwargs):

        code = self.get_object()
        try:
            user = User.verify_recovery_code(code.user.phone or code.user.email, code.code)
        except InvalidRecoveryCodeError as exp:
            return api_response_error({"detail": exp.message})
        except RecoveryCodeLockedError as exp:
            return api_response_error({"detail": exp.message})

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_password = serializer.validated_data.get("new_password")
        user.set_password(new_password)
        user.save()

        return api_response_success({"detail": "Password changed successfully. Please login to continue"})
