"""
ASGI config for myproject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.routing import websocket_urlpatterns

application = ProtocolTypeRouter({  # 	This class Routes requests by protocol type
    "http": get_asgi_application(), # Django’s built-in function to return an ASGI application instance to handle HTTP requests
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    )
})