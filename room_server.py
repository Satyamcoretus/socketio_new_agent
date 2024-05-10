import socketio
import uuid

sio = socketio.AsyncServer(async_mode='asgi',logger=True)
app = socketio.ASGIApp(sio)


rooms = {}  # Dictionary to store room information (clients in each room)

@sio.event
async def connect(sid,environ,auth):
    print(f'Client {sid} connected')
    if auth:
        print(f' authentication - {auth}')
    if environ:
        print(f'Environ is - {environ}')


@sio.event
async def create_room(sid):
    """
    client will create this room as soon as it will ask for the customer support in the chatbot
    :param sid: session id
    :return: None
    """
    room_id = str(uuid.uuid4())  # Generate a unique room ID
    rooms[room_id] = {sid}  # Add the connecting client to the room
    await sio.emit(event='room_created', data={'room_id': room_id}, to=sid)
    print(f'Client {sid} created room: {room_id}')

@sio.event
async def join_room(sid, room_id):
    if room_id in rooms:
        rooms[room_id].add(sid)  # Add client to the room
        # enter into the room
        await sio.enter_room(sid=sid,room=room_id)
        print(f'User [{sid}] entered the room - [{room_id}] ')

        await sio.emit(event='room_joined', data={'room_id': room_id}, to=sid)
        print(f'Client {sid} joined room: {room_id}')
        # Broadcast a message to existing clients in the room

    else:
        await sio.emit(event='room_error', data={'message': 'Room does not exist'}, to=sid)
        print(f'Client {sid} attempted to join non-existent room: {room_id}')

@sio.event
async def chat_message(sid, room_id, data):
    if room_id in rooms and sid in rooms[room_id]:
        # Broadcast the message to all clients in the room except the sender
        await sio.emit(event='message', data=data, room=room_id, skip_sid=sid)
        print(f'Client {sid} sent message in room {room_id}: {data}')
    else:
        await sio.emit(event='chat_error', data={'message': 'You are not in this room'}, to=sid)
        print(f'Client {sid} attempted to send message in non-existent room: {room_id}')

# @sio.event
# async def disconnect(sid):
#     # Remove the client from any rooms they were in
#     for room_id, clients in rooms.items():
#         if sid in clients:
#             clients.remove(sid)
#             if not clients:  # If the room becomes empty, remove it
#                 del rooms[room_id]
#             # Notify remaining clients in the room about the disconnection
#             await sio.emit(event='user_left', data={'message': f'{sid} has left the room'}, room=room_id)
#             print(f'Client {sid} disconnected from room: {room_id}')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=8000)
