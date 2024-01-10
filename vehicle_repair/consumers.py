

import json
from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
import time

coordinates = [
    [
        85.330293,
        27.703309
    ],
    [
        85.330328,
        27.703372
    ],
    [
        85.3304,
        27.703433
    ],
    [
        85.331427,
        27.703345
    ],
    [
        85.331973,
        27.7033
    ],
    [
        85.332081,
        27.70331
    ],
    [
        85.332267,
        27.703411
    ],
    [
        85.332441,
        27.703528
    ],
    [
        85.332502,
        27.703606
    ],
    [
        85.332652,
        27.703818
    ],
    [
        85.332654,
        27.703918
    ],
    [
        85.332944,
        27.703817
    ],
    [
        85.333931,
        27.703525
    ],
    [
        85.334216,
        27.703437
    ],
    [
        85.334465,
        27.703365
    ],
    [
        85.33565,
        27.703
    ],
    [
        85.335815,
        27.70294
    ],
    [
        85.336285,
        27.702783
    ],
    [
        85.336324,
        27.702876
    ],
    [
        85.336223,
        27.703198
    ],
    [
        85.33621,
        27.70327
    ],
    [
        85.33624,
        27.703666
    ],
    [
        85.336335,
        27.704733
    ],
    [
        85.336383,
        27.705381
    ],
    [
        85.33646,
        27.70561
    ],
    [
        85.336602,
        27.705891
    ],
    [
        85.336633,
        27.706071
    ],
    [
        85.336646,
        27.706264
    ],
    [
        85.336702,
        27.706534
    ],
    [
        85.336714,
        27.706775
    ],
    [
        85.336791,
        27.707216
    ],
    [
        85.336921,
        27.707803
    ],
    [
        85.337012,
        27.707917
    ],
    [
        85.337105,
        27.707961
    ],
    [
        85.337248,
        27.707985
    ],
    [
        85.337371,
        27.708052
    ],
    [
        85.338019,
        27.708024
    ],
    [
        85.33802,
        27.707937
    ],
    [
        85.338164,
        27.707612
    ]
]


class RepairRequestLocationConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['idx']
        self.room_group_name = 'repair_request_users_location_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()
        # self.send(text_data=json.dumps({
        #     'status': "connected from django channels"
        # }))

        for coordinate in coordinates:
            self.send(text_data=json.dumps({
                'location': coordinate
            }))

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

        # for coordinate in coordinates:
        #     self.send(text_data=json.dumps({
        #         'location': coordinate
        #     }))
        #     time.sleep(3)
