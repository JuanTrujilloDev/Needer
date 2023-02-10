from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('chat/<int:pk>', consumers.ChatConsumer.as_asgi()),
]