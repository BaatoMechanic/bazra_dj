from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from autho.models.recovery_code import RecoveryCode
from autho.serializers.recovery import SendRecoveryCodeSerializer
from utils.api_response import api_response_success
from utils.mixins.base_api_mixin import BaseAPIMixin


class AccountRecoveryViewSet(BaseAPIMixin, GenericViewSet):

    @action(detail=False, methods=["POST"])
    def send_otp(self, request, *args, **kwargs):
        serializer = SendRecoveryCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get("user_identifier")
        code: RecoveryCode = user.gen_recovery_code()
        code.send()

        return api_response_success({"detail": "OTP sent successfully."})

    @action(detail=False, methods=["POST"])
    def resend(self, request, *args, **kwargs):
        recovery_idx = request.data.get("idx")
        try:
            code = RecoveryCode.objects.get(idx=recovery_idx)

        except RecoveryCode.DoesNotExist:

            return api_response_success({"detail": "Resend the Otp again."})

        code.update_code()
        return api_response_success({"detail": "Resend sent successfully."})
