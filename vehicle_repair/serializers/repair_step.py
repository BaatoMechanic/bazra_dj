
from utils.mixins.serializer_mixins import BaseModelSerializerMixin
from vehicle_repair.models import RepairStep, RepairStepReport
from vehicle_repair.models.repair_step import RepairStepBillImage


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
    report = RepairStepReportSerializer()

    class Meta:
        model = RepairStep
        fields = ["idx", "name", "text_description", "audio_description", "status", "report"]
