from django.urls import path
from vehicle_repair.consumers import (
    RepairRequestMechanicLocationConsumer,
    RepairStepsConsumer,
    VehicleRepairRequestConsumer,
)

ws_patterns = [
    path(
        "repair-request/<idx>",
        VehicleRepairRequestConsumer.as_asgi(),
        name="websocket-repair-request",
    ),
    path(
        "repair-steps/<repair_idx>",
        RepairStepsConsumer.as_asgi(),
        name="websocket-repair-steps",
    ),
    # path("repair-steps/<idx>", RepairStepsConsumer.as_asgi(), name="websocket-repair-steps"),
    path(
        "repair-request-mechanic-location/<idx>",
        RepairRequestMechanicLocationConsumer.as_asgi(),
        name="websocket-mechanic-location",
    ),
]
