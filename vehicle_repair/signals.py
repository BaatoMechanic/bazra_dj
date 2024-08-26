from django.db.models.signals import post_save

from django.dispatch import receiver
from vehicle_repair.models.repair_step import RepairStep, RepairStepReport
from vehicle_repair.serializers.repair_step import RepairStepSerializer

from vehicle_repair.serializers.vehicle_repair_request import (
    VehicleRepairRequestSerializer,
)
from .models import VehicleRepairRequest

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(post_save, sender=VehicleRepairRequest)
def notify_repair_request_update(sender, **kwargs):
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        "repair_request_%s" % kwargs["instance"].idx,
        {
            "type": "repair_request_update",
            "value": VehicleRepairRequestSerializer(kwargs["instance"]).data,
        },
    )


@receiver(post_save, sender=RepairStep)
@receiver(post_save, sender=RepairStepReport)
def notify_repair_step_update(sender, **kwargs):
    channel_layer = get_channel_layer()
    instance = kwargs["instance"]
    # instance could be repair step or repair step report so getting repair request idx accordingly
    repair_request_idx = (
        instance.repair_request.idx if isinstance(instance, RepairStep) else instance.repair_step.repair_request.idx
    )
    repair_steps = RepairStep.objects.filter(repair_request__idx=repair_request_idx)

    async_to_sync(channel_layer.group_send)(
        "repair_steps_%s" % repair_request_idx,
        {
            "type": "repair_step_update",
            "value": RepairStepSerializer(repair_steps, many=True).data,
        },
    )
