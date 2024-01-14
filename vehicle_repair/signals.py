import json
from django.db.models.signals import post_save

from django.dispatch import receiver

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
            "value": json.dumps({
                "repair_request": json.dumps(VehicleRepairRequestSerializer(kwargs["instance"]).data)
            })
        }
    )
