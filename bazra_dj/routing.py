from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from vehicle_repair.consumers import VehicleRepairRequestConsumer, RepairRequestMechanicLocationConsumer, RepairStepsConsumer


ws_patterns = [
    path("repair-request/<idx>", VehicleRepairRequestConsumer.as_asgi(), name="websocket-repair-request"),
    path("repair-steps/<repair_idx>", RepairStepsConsumer.as_asgi(), name="websocket-repair-steps"),
    # path("repair-steps/<idx>", RepairStepsConsumer.as_asgi(), name="websocket-repair-steps"),
    path(
        "repair-request-mechanic-location/<idx>",
        RepairRequestMechanicLocationConsumer.as_asgi(),
        name="websocket-mechanic-location"),

]
