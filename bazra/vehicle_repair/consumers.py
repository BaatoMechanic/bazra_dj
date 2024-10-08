import json
from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
from autho.models.location import UserLocation
from autho.serializers.location import UserLocationSerializer
from vehicle_repair.models.repair_step import RepairStep

from vehicle_repair.models.vehicle_repair_request import VehicleRepairRequest
from vehicle_repair.serializers.repair_step import RepairStepSerializer
from vehicle_repair.serializers.vehicle_repair_request import (
    VehicleRepairRequestSerializer,
)

coordinates = [
    [
        85.330293,
        27.703309,
        "Kohalpur",
    ],
    [
        85.330328,
        27.703372,
        "Kohalpur",
    ],
    [
        85.3304,
        27.703433,
        "Kohalpur",
    ],
]


class VehicleRepairRequestConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["idx"]
        self.room_group_name = "repair_request_%s" % self.room_name

        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)

        self.accept()

        repair_request = VehicleRepairRequest.objects.get(idx=self.room_name)

        self.send(text_data=json.dumps(VehicleRepairRequestSerializer(repair_request).data))

        # for coordinate in coordinates:
        #     self.send(text_data=json.dumps({
        #         'location': coordinate
        #     }))

        # time.sleep(3)

    def receive(self, text_data=None, bytes_data=None):
        print(text_data)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)
        raise StopConsumer()

    def repair_request_update(self, event):
        self.send(text_data=json.dumps(event["value"]))


class RepairStepsConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["repair_idx"]
        self.room_group_name = "repair_steps_%s" % self.room_name

        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)

        self.accept()

        repair_steps = RepairStep.objects.filter(repair_request__idx=self.room_name)

        self.send(text_data=json.dumps(RepairStepSerializer(repair_steps, many=True).data))

    def receive(self, text_data=None, bytes_data=None):
        print(text_data)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)
        raise StopConsumer()

    def repair_step_update(self, event):
        self.send(text_data=json.dumps(event["value"]))


class RepairRequestMechanicLocationConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["idx"]
        self.room_group_name = "repair_request_mechanic_location_%s" % self.room_name

        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)

        self.accept()

        repair_request = VehicleRepairRequest.objects.get(idx=self.room_name)

        mechanic_location = (
            UserLocation.objects.filter(user=repair_request.assigned_mechanic.user).order_by("-created_at").first()
        )

        location = UserLocationSerializer(mechanic_location).data
        location["latitude"] = coordinates[0][1]
        location["longitude"] = coordinates[0][0]
        location["location_name"] = coordinates[0][2]

        self.send(text_data=json.dumps({"mechanic_location": location}))

    # def receive(self, text_data=None, bytes_data=None):
    # print(text_data)
    # self.send(text_data=json.dumps({"mechanic_location": text_data}))
    #
    #
    def receive(self, text_data=None, bytes_data=None):
        # Directly broadcast the message to all clients in the group
        print(text_data)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "broadcast_mechanic_location",
                "message": text_data,
            },
        )

    def broadcast_mechanic_location(self, event):
        message = event["message"]
        self.send(text_data=json.dumps({"mechanic_location": message}))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)
        raise StopConsumer()

    def notify_location_update(self, event):
        pass
        # self.send(text_data=json.dumps(event))

        for coordinate in coordinates:
            self.send(text_data=json.dumps({"location": coordinate}))
        # time.sleep(3)
