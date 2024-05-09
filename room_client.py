import asyncio
import socketio

loop = asyncio.get_event_loop()
sio = socketio.AsyncClient()


import asyncio
import socketio

sio = socketio.AsyncClient()

room_id = None  # Store the current room ID

@sio.event
async def connect():
    print('Connected to server')

@sio.event
async def room_created(data):
    global room_id
    room_id = data['room_id']
    print(f'Room created: {room_id}')

@sio.event
async def room_joined(data):
    global room_id
    room_id = data['room_id']
    print(f'Joined room: {room_id}')

@sio.event
async def room_error(data):
    print(f'Error: {data["message"]}')

@sio.event
async def user_joined(data):
    print(data['message'])

@sio.event
async def user_left(data):
    print(data['message'])

@sio.event
async def message(data):
    print(f'{data["message"]}')

