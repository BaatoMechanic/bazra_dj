from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from django.conf import settings
from rest_framework import status

from autho.exceptions import (
    InvalidVerificationCodeError,
    VerificationCodeLockedException,
)
from autho.models import User
from autho.models.verification_code import VerificationCode
from autho.serializers.recovery import (
    SendVerificationCodeSerializer,
    VerfiyVerificationOtpCodeSerializer,
)
from utils.api_response import api_response_error, api_response_success
from utils.mixins.base_api_mixin import BaseAPIMixin


class AccountVerificationViewSet(BaseAPIMixin, GenericViewSet):
    queryset = VerificationCode.objects.all()

    def get_serializer_class(self):
        if self.action == "send_otp_uid":
            return SendVerificationCodeSerializer
        if self.action == "verify_otp":
            return VerfiyVerificationOtpCodeSerializer

    @action(detail=False, methods=["POST"])
    def send_otp_uid(self, request, *args, **kwargs):

        uid = request.data.get("user_identifier")
        user = User.get_user_by_identifier(uid)
        if user is None:
            return api_response_error(
                {"detail": "User Not Found."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        code: VerificationCode = user.gen_verification_code()
        code.send()

        return api_response_success(
            {
                "verification": {
                    "idx": code.idx,
                },
                "message": "Please check your mobile and email for otp code ",
            }
        )

    @action(detail=False, methods=["POST"])
    def resend(self, request, *args, **kwargs):
        verification_idx = request.data.get("idx")
        try:
            code = VerificationCode.objects.get(idx=verification_idx)

        except VerificationCode.DoesNotExist:
            return api_response_error({"detail": "Resend the verification otp again."})

        code.update_code()
        return api_response_success({"detail": "Verification otp resent successfully."})

    @action(detail=False, methods=["POST"])
    def check_otp(self, request, *args, **kwargs):
        if settings.STAGING:
            return api_response_success({"detail": "Valid otp"})
        code = VerificationCode.objects.filter(idx=request.data.get("otp")).first()

        if code and code.code == request.data.get("code"):
            return api_response_success({"detail": "Valid otp"})

        return api_response_error({"detail": "Invalid otp"})

    @action(detail=True, methods=["POST"])
    def verify_otp(self, request, *args, **kwargs):
        code = self.get_object()
        try:
            user = User.verify_verification_code(
                code.user.phone or code.user.email, code.code
            )
        except InvalidVerificationCodeError as exp:
            return api_response_error({"detail": exp.message})
        except VerificationCodeLockedException as exp:
            return api_response_error({"detail": exp.message})

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_password = serializer.validated_data.get("new_password")
        user.set_password(new_password)
        user.save()

        return api_response_success({"detail": "Verification successful."})
