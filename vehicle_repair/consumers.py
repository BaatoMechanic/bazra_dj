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
    [
        85.331427,
        27.703345,
        "Kohalpur",
    ],
    [
        85.331973,
        27.7033,
        "Kohalpur",
    ],
    [
        85.332081,
        27.70331,
        "Kohalpur",
    ],
    [
        85.332267,
        27.703411,
        "Kohalpur",
    ],
    [
        85.332441,
        27.703528,
        "Kohalpur",
    ],
    [
        85.332502,
        27.703606,
        "Kohalpur",
    ],
    [
        85.332652,
        27.703818,
        "Kohalpur",
    ],
    [
        85.332654,
        27.703918,
        "Kohalpur",
    ],
    [
        85.332944,
        27.703817,
        "Kohalpur",
    ],
    [
        85.333931,
        27.703525,
        "Kohalpur",
    ],
    [
        85.334216,
        27.703437,
        "Kohalpur",
    ],
    [
        85.334465,
        27.703365,
        "Kohalpur",
    ],
    [
        85.33565,
        27.703,
        "Kohalpur",
    ],
    [
        85.335815,
        27.70294,
        "Kohalpur",
    ],
    [
        85.336285,
        27.702783,
        "Kohalpur",
    ],
    [
        85.336324,
        27.702876,
        "Kohalpur",
    ],
    [
        85.336223,
        27.703198,
        "Kohalpur",
    ],
    [
        85.33621,
        27.70327,
        "Kohalpur",
    ],
    [
        85.33624,
        27.703666,
        "Kohalpur",
    ],
    [
        85.336335,
        27.704733,
        "Kohalpur",
    ],
    [
        85.336383,
        27.705381,
        "Kohalpur",
    ],
    [
        85.33646,
        27.70561,
        "Kohalpur",
    ],
    [
        85.336602,
        27.705891,
        "Kohalpur",
    ],
    [
        85.336633,
        27.706071,
        "Kohalpur",
    ],
    [
        85.336646,
        27.706264,
        "Kohalpur",
    ],
    [
        85.336702,
        27.706534,
        "Kohalpur",
    ],
    [
        85.336714,
        27.706775,
        "Kohalpur",
    ],
    [
        85.336791,
        27.707216,
        "Kohalpur",
    ],
    [
        85.336921,
        27.707803,
        "Kohalpur",
    ],
    [
        85.337012,
        27.707917,
        "Kohalpur",
    ],
    [
        85.337105,
        27.707961,
        "Kohalpur",
    ],
    [
        85.337248,
        27.707985,
        "Kohalpur",
    ],
    [
        85.337371,
        27.708052,
        "Kohalpur",
    ],
    [
        85.338019,
        27.708024,
        "Kohalpur",
    ],
    [
        85.33802,
        27.707937,
        "Kohalpur",
    ],
    [
        85.338164,
        27.707612,
        "Kohalpur",
    ],
]


class VehicleRepairRequestConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["idx"]
        self.room_group_name = "repair_request_%s" % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

        repair_request = VehicleRepairRequest.objects.get(idx=self.room_name)

        self.send(
            text_data=json.dumps(VehicleRepairRequestSerializer(repair_request).data)
        )

        # for coordinate in coordinates:
        #     self.send(text_data=json.dumps({
        #         'location': coordinate
        #     }))

        # time.sleep(3)

    def receive(self, text_data=None, bytes_data=None):
        print(text_data)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        raise StopConsumer()

    def repair_request_update(self, event):
        self.send(text_data=json.dumps(event["value"]))


class RepairStepsConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["repair_idx"]
        self.room_group_name = "repair_steps_%s" % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

        repair_steps = RepairStep.objects.filter(repair_request__idx=self.room_name)

        self.send(
            text_data=json.dumps(RepairStepSerializer(repair_steps, many=True).data)
        )

    def receive(self, text_data=None, bytes_data=None):
        print(text_data)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        raise StopConsumer()

    def repair_step_update(self, event):
        self.send(text_data=json.dumps(event["value"]))


class RepairRequestMechanicLocationConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["idx"]
        self.room_group_name = "repair_request_mechanic_location_%s" % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

        repair_request = VehicleRepairRequest.objects.get(idx=self.room_name)

        mechanic_location = (
            UserLocation.objects.filter(user=repair_request.assigned_mechanic.user)
            .order_by("-created_at")
            .first()
        )

        location = UserLocationSerializer(mechanic_location).data
        location["latitude"] = coordinates[0][1]
        location["longitude"] = coordinates[0][0]
        location["location_name"] = coordinates[0][2]

        self.send(text_data=json.dumps({"mechanic_location": location}))

        # for coordinate in coordinates:
        #     self.send(text_data=json.dumps({
        #         'location': coordinate
        #     }))

        # time.sleep(3)

    def receive(self, text_data=None, bytes_data=None):
        print(text_data)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        raise StopConsumer()

    def notify_location_update(self, event):
        pass
        # self.send(text_data=json.dumps(event))

        for coordinate in coordinates:
            self.send(text_data=json.dumps({"location": coordinate}))
        # time.sleep(3)
