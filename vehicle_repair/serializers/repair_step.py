from rest_framework import serializers

from utils.mixins.serializer_model_mixins import BaseModelSerializerMixin
from vehicle_repair.models import RepairStep, RepairStepReport, RepairStepBillImage, VehicleRepairRequest


class RepairStepBillImageSerializer(BaseModelSerializerMixin):

    class Meta:
        model = RepairStepBillImage
        fields = ["idx", "image",]


class RepairStepReportSerializer(BaseModelSerializerMixin):
    bill_images = RepairStepBillImageSerializer(many=True, read_only=True)

    class Meta:
        model = RepairStepReport
        fields = ["idx", "bill_images"]


class RepairStepSerializer(BaseModelSerializerMixin):
    report = RepairStepReportSerializer(required=False)

    class Meta:
        model = RepairStep
        fields = ["idx", "name", "text_description", "audio_description", "status", "report"]


class CreateRepairStepSerializer(BaseModelSerializerMixin):
    report = RepairStepReportSerializer(required=False)
    repair_request = serializers.CharField()

    class Meta:
        model = RepairStep
        fields = ["idx", "repair_request", "name", "text_description", "audio_description", "status", "report"]

    def create(self, validated_data):
        repair_request_idx = validated_data.pop('repair_request')
        repair_request = VehicleRepairRequest.objects.get(idx=repair_request_idx)
        validated_data['repair_request'] = repair_request
        return super().create(validated_data)
