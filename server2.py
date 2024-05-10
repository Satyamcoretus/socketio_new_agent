import socketio
import uvicorn
from socketio import AsyncServer
from fastapi import FastAPI
fastapi_instance= FastAPI()
sio = AsyncServer(cors_allowed_origins='*',async_mode='asgi')
app = socketio.ASGIApp(sio,fastapi_instance)


@sio.event
async def communication_channel(sid,data=None):
    if data:
        print(f'received data from client {sid} input - {data}')
        response = f'get back your input to you [{data}]'
        await sio.emit(event='receiver_from_server', data=response)
        print(f'message {response} sent to client,...')
    print('---------------------------')



@sio.event
async def connect(sid,auth,environ):
    if auth:
        print(auth)
    if environ:
        print(environ)
    print(f'received sid {sid} from the client')
    await sio.emit(event='receiver_from_server',data = f'connection successful at sid {sid}')


if __name__ == '__main__':
    uvicorn.run('server2:app',port=8001,reload=True)



