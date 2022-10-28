import os
import socketio

async_mode = 'gevent'
basedir = os.path.dirname(os.path.realpath(__file__))
sio = socketio.Server(
    async_mode=async_mode,
    cors_allowed_origins='*'
)


users = {}

@sio.event
def set_username(sid, message):
    print(users)
    users[sid] = message['data']
    sio.emit('my_res', {'data': f"Username {users[sid]}"}, to=sid)
