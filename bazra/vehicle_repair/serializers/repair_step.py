from django.db.models.signals import post_save
from rest_framework import serializers

from utils.mixins.serializer_model_mixins import BaseModelSerializerMixin
from vehicle_repair.models import (
    RepairStep,
    RepairStepReport,
    RepairStepBillImage,
    VehicleRepairRequest,
)


class RepairStepBillImageSerializer(BaseModelSerializerMixin):

    class Meta:
        model = RepairStepBillImage
        fields = [
            "idx",
            "image",
        ]


class RepairStepReportSerializer(BaseModelSerializerMixin):

    bill_images = RepairStepBillImageSerializer(many=True)

    class Meta:
        model = RepairStepReport
        fields = ["idx", "bill_images"]


class CreateRepairStepReportSerializer(BaseModelSerializerMixin):

    bill_images = serializers.ListField(child=serializers.ImageField(), required=False, write_only=True)

    class Meta:
        model = RepairStepReport
        fields = ["idx", "bill_images"]

    def create(self, validated_data):

        repair_request_idx = self.context.get("repair_request_idx")
        repair_request = VehicleRepairRequest.objects.filter(idx=repair_request_idx).first()
        if not repair_request:
            raise serializers.ValidationError({"detail": "Repair request does not exist."})
        repair_step_idx = self.context.get("repair_step_idx")
        repair_step = RepairStep.objects.filter(idx=repair_step_idx).first()
        if not repair_step:
            raise serializers.ValidationError({"detail": "Repair step does not exist."})
        validated_data["repair_step"] = repair_step
        bill_images = validated_data.pop("bill_images", None)
        instance = super().create(validated_data)
        images = []

        if bill_images:
            for bill_image in bill_images:
                image = RepairStepBillImage(report=instance, image=bill_image)
                images.append(image)
        RepairStepBillImage.objects.bulk_create(images)
        # since bulk_create does not trigger post_save signals so triggering it here manually
        post_save.send(sender=RepairStepReport, instance=instance, created=True)
        return instance


class RepairStepSerializer(BaseModelSerializerMixin):

    report = RepairStepReportSerializer(required=False)

    class Meta:
        model = RepairStep
        fields = [
            "idx",
            "name",
            "text_description",
            "audio_description",
            "status",
            "report",
        ]
        serializers = {"report": RepairStepReportSerializer}

    def create(self, validated_data):
        repair_request_idx = self.context.get("repair_request_idx")
        repair_request = VehicleRepairRequest.objects.filter(idx=repair_request_idx).first()
        if not repair_request:
            raise serializers.ValidationError({"detail": "Repair request does not exist."})
        validated_data["repair_request"] = repair_request
        return super().create(validated_data)
