from django.http import HttpRequest

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny

from autho.models import User
from autho.serializers import UserLocationSerializer, UserRegistrationSerializer

from utils.api_response import api_response_error, api_response_success
from utils.mixins.base_api_mixin import BaseAPIMixin


class UserManagementViewSet(BaseAPIMixin, GenericViewSet):
    """
    This file is responsible to perform all the user registration and info change logic for the project.
    Any user info modification logic should be added here.
    """

    @action(detail=False, methods=["POST"], permission_classes=[AllowAny])
    def register(self, request: HttpRequest) -> Response:
        """
        Register the user.

        Args:
            request (Request): The request object.

        Returns:
            Response: The response object.
        """
        serializer: UserRegistrationSerializer = UserRegistrationSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user: User = serializer.save()
            code = user.gen_verification_code()
            code.meta.update(
                {
                    # saving identifier to meta becaus user can't be compared in case of account verification so to
                    # to make sure the code was generated specifically for the user with this identifier, we are
                    # adding it to meta
                    "identifier": serializer.validated_data["user_identifier"],
                    "is_account_verification": True,
                }
            )
            code.save()
            code.send()
            return api_response_success(
                {
                    "verification": {
                        "idx": code.idx,
                    },
                    "message": "Please check your mobile and email for otp code ",
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return api_response_error({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # @action(detail=False, methods=["POST"])
    # def identifier_verification_token(self, request: HttpRequest) -> Response:

    #     identifier = request.data.get("user_identifier")
    #     user = request.user
    #     is_email = is_valid_email(identifier)
    #     if user is None:
    #         return api_response_error(
    #             {
    #                 "detail": f"No user found with this {'email' if is_email else 'number'}"
    #             },
    #             status=status.HTTP_400_BAD_REQUEST,
    #         )
    #     if (
    #         is_email
    #         and user.is_email_verified
    #         or (not is_email)
    #         and user.is_phone_verified
    #     ):
    #         return api_response_error(
    #             {"detail": f"{'Email' if is_email else 'Number'} already verified."},
    #             status=status.HTTP_400_BAD_REQUEST,
    #         )
    #     code = VerificationCode.generate_verification_code(user)
    #     user.meta.update(
    #         {f"{'email' if is_email else 'phone'}_verification_code": code.idx}
    #     )
    #     setattr(user, f"{'email' if is_email else 'phone'}", identifier)
    #     user.save()
    #     return api_response_success(
    #         {
    #             "verification": {
    #                 "idx": code.idx,
    #             },
    #             "message": f"Please check your {'email' if is_email else 'phone'} for otp code ",
    #         }
    #     )

    # @action(detail=False, methods=["POST"])
    # def verify_identifier(self, request: HttpRequest) -> Response:
    #     """
    #     Verify a user.

    #     Args:
    #         request (Request): The request object.

    #     Returns:
    #         Response: The response object.
    #     """
    #     user = request.user
    #     identifier = request.data.get("user_identifier")
    #     code_number = request.data.get("code")
    #     is_email = is_valid_email(identifier)

    #     if not user:
    #         return api_response_error(
    #             {
    #                 "detail": f"No user found with this {'email' if is_email else 'number'}."
    #             },
    #             status=status.HTTP_400_BAD_REQUEST,
    #         )
    #     code_field = ("email_verification_code" if is_email else "phone_verification_code")

    #     code = VerificationCode.objects.filter(
    #         user=user, idx=user.meta.get(code_field)
    #     ).first()
    #     if not code or not code.equals(code_number):
    #         if code:
    #             user.verification_code.increment_retries()
    #         return api_response_error(
    #             {"detail": "Invalid code"},
    #             status=status.HTTP_400_BAD_REQUEST,
    #         )
    #     if is_email:
    #         user.is_email_verified = True
    #     else:
    #         user.is_phone_verified = True
    #     user.save(update_fields=[f"is_{'email' if is_email else 'phone'}_verified"])
    #     code.delete()
    #     return api_response_success(
    #         {"message": f"{'Email' if is_email else 'Number'} verified successfully."}
    #     )

    @action(detail=False, methods=["DELETE"])
    def delete_user(self, request: HttpRequest) -> Response:
        """
        Delete a user.

        Args:
            request (Request): The request object.

        Returns:
            Response: The response object.
        """

        user: User = request.user
        user.delete()
        return api_response_success({"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["POST"])
    def update_location(self, request: HttpRequest) -> Response:
        """
        Update a user's location.

        Args:
            request (Request): The request object.

        Returns:
            Response: The response object.
        """

        serializer = UserLocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return api_response_success(serializer.data)

    @action(detail=False, methods=["POST"])
    def change_password(self, request: HttpRequest) -> Response:
        """
        Update a user's password.

        Args:
            request (Request): The request object.

        Returns:
            Response: The response object.
        """

        user: User = request.user
        is_correct = user.check_password(request.data.get("old_password"))
        if is_correct:
            new_password = request.data.get("new_password")
            if not new_password:
                return api_response_error(
                    {"detail": "New password cannot be empty."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.set_password(new_password)
            user.save()
            return api_response_success({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)
        else:
            return api_response_error(
                {"detail": "Old password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST,
            )
