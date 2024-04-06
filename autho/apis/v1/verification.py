from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from django.conf import settings

from autho.exceptions import (
    InvalidVerificationCodeError,
    UserAlreadyVerifiedError,
    VerificationCodeLockedError,
)
from autho.models import User
from autho.models.verification_code import VerificationCode
from autho.serializers.recovery import (
    SendVerificationCodeSerializer,
    VerfiyAccounSerializer,
    VerfiyVerificationOtpCodeSerializer,
)
from permission.models import Role
from utils.api_response import api_response_error, api_response_success
from utils.helpers import check_identifier_is_email
from utils.mixins.base_api_mixin import BaseAPIMixin


class AccountVerificationViewSet(BaseAPIMixin, GenericViewSet):
    queryset = VerificationCode.objects.all()

    def get_serializer_class(self):
        if self.action == "send_otp_uid":
            return SendVerificationCodeSerializer
        if self.action == "verify_otp":
            return VerfiyVerificationOtpCodeSerializer
        if self.action == "verify_account_otp":
            return VerfiyAccounSerializer

    @action(detail=False, methods=["POST"])
    def send_otp_uid(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        is_account_verification = serializer.validated_data["for_account_verification"]
        uid = serializer.validated_data["user_identifier"]
        try:
            code: VerificationCode = user.gen_verification_code(
                is_account_verification=is_account_verification
            )
        except UserAlreadyVerifiedError as exp:
            return api_response_error({"detail": exp.message})
        code.meta.update(
            {
                "identifier": uid,
                "is_account_verification": is_account_verification,
            }
        )
        code.save()
        code.send()

        if check_identifier_is_email(uid):
            user.email = uid
            user.save(update_fields=["email"])
        else:
            user.phone = uid
            user.save(update_fields=["phone"])

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

        # code = VerificationCode.objects.filter(idx=request.data.get("otp")).first()
        code = self.get_object()

        if code and code.code == request.data.get("code"):
            return api_response_success({"detail": "Valid otp"})

        return api_response_error({"detail": "Invalid otp"})

    @action(detail=True, methods=["POST"])
    def verify_account_otp(self, request, *args, **kwargs):
        code = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data.get("for_account_verification") != code.meta.get(
            "is_account_verification"
        ):
            return api_response_error({"detail": "Invalid request"})

        identifier = serializer.validated_data.get("user_identifier")
        if identifier != code.meta.get("identifier"):
            return api_response_error({"detail": "Invalid request"})
        otp_code = serializer.validated_data.get("otp_code")
        new_password = serializer.validated_data.get("new_password")
        otp_code = serializer.validated_data.get("otp_code")
        is_email = check_identifier_is_email(identifier)
        try:
            user = User.verify_verification_code(identifier, otp_code)
        except InvalidVerificationCodeError as exp:
            return api_response_error({"detail": exp.message})
        except VerificationCodeLockedError as exp:
            return api_response_error({"detail": exp.message})

        user.set_password(new_password)
        setattr(user, f"{'email' if is_email else 'phone'}", identifier)
        user.is_verified = True
        # Add the consumer Role to the user after the verification
        r = Role.objects.get(name="Consumer")
        user.add_roles(r)
        user.save(
            update_fields=[
                f"{'email' if is_email else 'phone'}",
                "is_verified",
                "password",
            ]
        )
        return api_response_success(
            {
                "user_idx": user.idx,
                "detail": "Verification successful.",
            }
        )

    @action(detail=True, methods=["POST"])
    def verify_otp(self, request, *args, **kwargs):
        code = self.get_object()
        request_user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data.get("for_account_verification") != code.meta.get(
            "is_account_verification"
        ):
            return api_response_error({"detail": "Invalid request"})
        identifier = serializer.validated_data.get("user_identifier")
        otp_code = serializer.validated_data.get("otp_code")
        if not identifier or identifier != code.meta.get("identifier"):
            return api_response_error({"detail": "Invalid verification code."})
        is_email = check_identifier_is_email(identifier)
        try:
            user = User.verify_verification_code(identifier, otp_code)
            if request_user.id != user.id:
                return api_response_error({"detail": "Invalid verification code."})
        except InvalidVerificationCodeError as exp:
            return api_response_error({"detail": exp.message})
        except VerificationCodeLockedError as exp:
            return api_response_error({"detail": exp.message})

        if is_email:
            user.is_email_verified = True
        else:
            user.is_phone_verified = True
        user.save(update_fields=[f"is_{'email' if is_email else 'phone'}_verified"])

        return api_response_success(
            {
                "user_idx": user.idx,
                "detail": f"Your {'email' if is_email else 'phone number'} has been verified successfully.",
            }
        )
