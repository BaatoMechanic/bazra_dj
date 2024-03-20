from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from autho.models.recovery_code import RecoveryCode
from autho.serializers.recovery import SendRecoveryCodeSerializer
from utils.api_response import api_response_success
from utils.mixins.base_model_mixin import BaseModelMixin


class AccountRecoveryViewSet(BaseModelMixin, GenericViewSet):

    @action(detail=False, methods=["POST"])
    def send_otp(self, request):
        serializer = SendRecoveryCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get("user_identifier")

        code: RecoveryCode = user.gen_recovery_code()

        code.send()

        return api_response_success({"detail": "OTP sent successfully."})
