from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from vehicle_repair.consumers import RepairRequestLocationConsumer


ws_patterns = [
    path("repair_userslocation/<idx>", RepairRequestLocationConsumer.as_asgi(), name="users_location"),

]
