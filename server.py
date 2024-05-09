import uvicorn
from socketio import Server
from fastapi import FastAPI


from fastapi.responses import HTMLResponse
sio = Server()

app = FastAPI()



@sio.on('connect')
def connect(sid,environ,auth):
    # connect function
    print(f'connection is establised with sid {sid}')
    if auth:
        print(f'authentification info {auth}')
    if environ:
        print(f'environ info {environ}')


@sio.on('disconnect')
def disconnect(sid):
    # disconnect function
    pass


@sio.on('click_button')
def create_room(sid,room_id):
    sio.enter_room(sid,room=room_id)
    print('Enter into the room ')
    session_info = sio.get_session(sid)
    print(f'session info of user having sid {sid} is {session_info}')


if __name__ == '__main__':
    uvicorn.run('server:app',port=8001,reload=True)

