from django.urls import  path, re_path
from . import consumers

websocket_urlpatterns = [
re_path(r'ws/tris(?:/(?P<room_name>[^/]+))?/?$', consumers.TrisConsumer.as_asgi())

]
