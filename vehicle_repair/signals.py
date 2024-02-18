import json
from django.db.models.signals import post_save

from django.dispatch import receiver
from vehicle_repair.models.repair_step import RepairStep
from vehicle_repair.serializers.repair_step import RepairStepSerializer

from vehicle_repair.serializers.vehicle_repair_request import VehicleRepairRequestSerializer
from .models import VehicleRepairRequest

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(post_save, sender=VehicleRepairRequest)
def notify_repair_request_update(sender, **kwargs):
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        'repair_request_%s' % kwargs["instance"].idx, {
            "type": "repair_request_update",
            "value": VehicleRepairRequestSerializer(kwargs["instance"]).data
            })

@receiver(post_save, sender=RepairStep)
def notify_repair_step_update(sender, **kwargs):
    channel_layer = get_channel_layer()
    repair_steps = RepairStep.objects.filter( repair_request__idx = kwargs["instance"].repair_request.idx)

    async_to_sync(channel_layer.group_send)(
        'repair_steps_%s' % kwargs["instance"].repair_request.idx, {
            "type": "repair_step_update",
            "value": RepairStepSerializer(repair_steps, many=True).data
        }
    )
