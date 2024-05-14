import asyncio
import socketio
from room_server import ChatNamespace
loop = asyncio.get_event_loop()
sio = socketio.AsyncClient(logger=True,engineio_logger=True)




# async def initiator():
#     print('initiator is called')
#     #emit to the server, it will generate a new room key for the client
#     await sio.emit(event='connect',namespace='/Chat')

# to emit room_id to server to that server can enter the user in the room
async def join_room():
    print('join_room is called')
    sio.emit(event='join',namespace='/Chat')

async def get_input():
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, input, "Enter a message to send to the server: ")


sio.event(namespace='/Chat')
async def disconnect_message(data):
    print(data)

async def send_message(message):
    await sio.emit(event='message',data=message,namespace='/Chat')

@sio.event(namespace='/Chat')
async def message_on_client(data):
    if isinstance(data,str):
        print('AGENT-')
        print(data)
    else:
        message = data.get('message')
        print(message)


async def main():
    await sio.connect('http://192.168.0.53:8000',namespaces='/Chat')
    # await initiator()
    await sio.emit(event='join',namespace='/Chat')
    while True:
        message_to_send = await get_input()
        await send_message(message_to_send)
        await asyncio.sleep(0.5)

#
if __name__ == '__main__':
    asyncio.run(main())