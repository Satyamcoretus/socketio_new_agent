import socketio
import uvicorn
from socketio import AsyncServer
from fastapi import FastAPI
fast_instance = FastAPI()
sio = AsyncServer(cors_allowed_origins='*',async_mode='asgi')
app = socketio.ASGIApp(sio)

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



