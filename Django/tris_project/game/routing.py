from django.urls import  path, re_path
from . import consumers

websocket_urlpatterns = [
    path("ws/tris/", consumers.TrisConsumer.as_asgi()),
]
