import uvicorn
from socketio import Server
from fastapi import FastAPI


from fastapi.responses import HTMLResponse
sio = Server()

app = FastAPI(sio)


@app.get("/items/", response_class=HTMLResponse)
async def read_items():
    with open('static/room.html', 'r') as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

@app.get('/chatbox',response_class=HTMLResponse)
async def chatbox_page():
    with open('static/chatbox.html', 'r') as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

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
    uvicorn.run('server:app',host='127.0.0.1',port=8001,reload=True)

