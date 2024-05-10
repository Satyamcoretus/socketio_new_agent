import asyncio
import socketio

loop = asyncio.get_event_loop()
sio = socketio.AsyncClient(logger=True, engineio_logger=True,reconnection_attempts=4)

room_id = None  # Store the current room ID


async def initiator():              # It will send the first ping to the server
    #emit to the server, it will generate a new room key for the client
    await sio.emit(event='create_room')


@sio.event
async def connect():
    print('Connection established')
    await initiator()



@sio.event
async def room_created(data):
    global room_id
    room_id = data['room_id']
    print(f'Room created: {room_id}')
#
@sio.event
async def room_joined(data):
    global room_id
    room_id = data['room_id']
    print(f'Joined room: {room_id}')

@sio.event
async def room_error(data):
    print(f'Error: {data["message"]}')


# @sio.event
# async def user_left(data):
#     print(data['message'])
#
# @sio.event
# async def message(data):
#     print(f'{data["message"]}')



async def main():
    await sio.connect('http://localhost:8000',transports='polling')
    await sio.wait()



if __name__ == '__main__':
    loop.run_until_complete(main())