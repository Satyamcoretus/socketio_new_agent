import uvicorn

import socketio

sio = socketio.AsyncServer(async_mode='asgi')
app = socketio.ASGIApp(sio)


@sio.event
async def ping_pong_from_server(sid):
    print(f'ping received from client - {sid}')
    data = 'take it chatar matar'
    await sio.emit(event='pong_from_server',data=data,to=sid)




if __name__ == '__main__':
    uvicorn.run(app, host='192.168.0.53', port=5000)

