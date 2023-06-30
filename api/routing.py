from django.urls import path, re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from . import consumers
from django.core.asgi import get_asgi_application

websocket_urlpatterns = [
    path('api/chat/send/<int:id>', consumers.ChatConsumer.as_asgi()),
    path('api/chat/send/', consumers.ChatConsumer.as_asgi()),
]


