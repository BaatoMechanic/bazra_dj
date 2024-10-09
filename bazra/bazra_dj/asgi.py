"""
ASGI config for bazra_dj project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
import django

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack


# Set the default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bazra_dj.settings")

# Ensure the app registry is loaded before importing other modules
django.setup()

from .routing import ws_patterns  # noqa

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(URLRouter(ws_patterns)),
    }
)
