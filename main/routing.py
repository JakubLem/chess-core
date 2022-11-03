# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
# from api import routing
# 
# 
# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     'websocket': AuthMiddlewareStack(
#         URLRouter(
#             routing.websocket_urlpatterns
#         )
#     ),
# })


from channels.routing import ProtocolTypeRouter, URLRouter
# import app.routing
from django.urls import re_path
from api.consumers import TextRoomConsumer
websocket_urlpatterns = [
    re_path(r'^ws/(?P<room_name>[^/]+)/$', TextRoomConsumer.as_asgi()),
]
# the websocket will open at 127.0.0.1:8000/ws/<room_name>
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket':
        URLRouter(
            websocket_urlpatterns
        )
    ,
})