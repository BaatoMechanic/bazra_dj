from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.request import HttpRequest
from rest_framework.viewsets import GenericViewSet
from django.conf import settings

from autho.exceptions import (
    InvalidVerificationCodeError,
    UserAlreadyVerifiedError,
    VerificationCodeLockedError,
)
from autho.models import User
from autho.models.verification_code import VerificationCode
from autho.serializers.recovery import VerifyOtpSerializer

from permission.models import Role
from utils.api_response import api_response_error, api_response_success
from utils.helpers import is_valid_email
from utils.mixins.base_api_mixin import BaseAPIMixin


class VerificationCodeViewSet(BaseAPIMixin, GenericViewSet):
    queryset = VerificationCode.objects.all()
    serializer_class = VerifyOtpSerializer

    @action(detail=False, methods=["POST"])
    def send_otp_uid(self, request, *args, **kwargs):
        """
        Send OTP code with the use of user identifier
        """
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        is_account_verification = serializer.validated_data["for_account_verification"]
        uid = serializer.validated_data["user_identifier"]
        try:
            code: VerificationCode = user.gen_verification_code(is_account_verification=is_account_verification)
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

        if is_valid_email(uid):
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

    @action(detail=True, methods=["POST"], permission_classes=[AllowAny])
    def check_otp(self, request, *args, **kwargs):
        """
        Account Verification ~ Check OTP
        Checks if the otp is valid or not for both the cases, user_identifier verification and account verification
        Note: account verification is needed while registring the user. But identifier verification is needed while
        verifying the idendifiers such as email and phone.
        """
        if settings.STAGING:
            if request.data.get("code") == "123456":
                return api_response_success({"detail": "Valid otp"})
            return api_response_error({"detail": "Invalid otp"})

        code = self.get_object()

        if code and code.code == request.data.get("code"):
            return api_response_success({"detail": "Valid otp"})

        return api_response_error({"detail": "Invalid otp"})

    @action(detail=True, methods=["POST"])
    def verify_otp(self, request: HttpRequest, *args, **kwargs):

        def verify_account_creation(request: HttpRequest):
            new_password = request.data.get("new_password")
            if not new_password:
                return api_response_error({"detail": "Password is required"})

            if len(new_password) < 8:
                return api_response_error({"detial": "Password must be at least 8 characters"})

            is_email = is_valid_email(identifier)

            user.set_password(new_password)
            setattr(user, f"{'email' if is_email else 'phone'}", identifier)
            user.is_verified = True
            if is_email:
                user.is_email_verified = True
            else:
                user.is_phone_verified = True

            # Add the consumer Role to the user after the verification
            r = Role.objects.get(name="Consumer")
            user.add_roles(r)
            user.primary_role = r
            user.save(
                update_fields=[
                    f"{'email' if is_email else 'phone'}",
                    f"is_{'email' if is_email else 'phone'}_verified",
                    "primary_role",
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

        def verify_user_identifier():
            is_email = is_valid_email(identifier)
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

        code = self.get_object()
        request_user = request.user

        if request_user.is_authenticated and request_user != code.user:
            return api_response_error({"detail": "Invalid verification code."})

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        is_account_verification = serializer.validated_data.get("for_account_verification")
        if is_account_verification != code.meta.get("is_account_verification"):
            return api_response_error({"detail": "Invalid request"})

        # Using identifier here even though identifier is not required here just to
        # make sure the code was generated for the same user even though code might
        # match by accident
        # ps: we can't compare request.user with code.user because user might
        # be annonymous (in case of account verification)
        identifier = serializer.validated_data.get("user_identifier")
        if identifier != code.meta.get("identifier"):
            return api_response_error({"detail": "Invalid verification code."})

        otp_code = serializer.validated_data.get("otp_code")
        try:
            user: User = User.verify_verification_code(identifier, otp_code)
            # if  request_user.id != user.id:
            #    # return api_response_error({"detail": "Invalid verification code."})
        except InvalidVerificationCodeError as exp:
            return api_response_error({"detail": exp.message})
        except VerificationCodeLockedError as exp:
            return api_response_error({"detail": exp.message})

        if is_account_verification:
            return verify_account_creation(request)

        return verify_user_identifier()
