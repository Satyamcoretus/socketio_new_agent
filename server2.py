import socketio
import uvicorn
from socketio import AsyncServer
from fastapi import FastAPI
fastapi_instance= FastAPI()
sio = AsyncServer(cors_allowed_origins='*',async_mode='asgi')
app = socketio.ASGIApp(sio,fastapi_instance)


@sio.event
async def communication_channel(sid,data):
    if data:
        print('---------------------------')
        print(f'data received from client {sid} - {data}')
    response = 'From server' + data
    await sio.emit(event='receiver_from_server',data=response)

@sio.event
async def connect(sid,auth,environ):
    if auth:
        print(auth)
    if environ:
        print(environ)
    print(f'received sid {sid} from the client')
    await sio.emit(f'connection successful at sid {sid}')


if __name__ == '__main__':
    uvicorn.run('server2:app',port=8001,reload=True)



