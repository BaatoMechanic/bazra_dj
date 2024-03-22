import json
from django.http import HttpRequest
from rest_framework import status
from autho.serializers.location import UserLocationSerializer
from autho.serializers.user_registration import UserRegistrationSerializer


from rest_framework.decorators import action
from utils.api_response import api_response_error, api_response_success


from utils.mixins.base_api_mixin import BaseAPIMixin

from rest_framework.response import Response

from rest_framework.viewsets import GenericViewSet

from autho.models import User

# @api_view(["POST"])
# @renderer_classes([JSONRenderer])
# @permission_classes((BazraPermission, ))
# def register_user(request, *args, **kwargs):
#     data = request.data.copy()


class UserManagementViewSet(BaseAPIMixin, GenericViewSet):
    """
    This file is responsible to perform all the user registration and info change logic for the project.
    Any user info modification logic should be added here.
    """

    @action(detail=False, methods=["POST"])
    def register(self, request: HttpRequest) -> Response:
        """
        Register a user.

        Args:
            request (Request): The request object.

        Returns:
            Response: The response object.
        """
        serializer: UserRegistrationSerializer = UserRegistrationSerializer(
            data=request.data
        )
        try:
            serializer.is_valid(raise_exception=True)
            response: json = serializer.save()
            return api_response_success(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            return api_response_error(
                {"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )

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
        return api_response_success(
            {"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT
        )

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
            return api_response_success(
                {"detail": "Password updated successfully."}, status=status.HTTP_200_OK
            )
        else:
            return api_response_error(
                {"detail": "Old password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST,
            )
