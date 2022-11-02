# source: https://github.com/veryacademy/YT-Django-Project-Chatroom-Getting-Started

from django.urls import re_path
from . import cunsumers


websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', cunsumers.ChatRoomConsumer),
]
