import asyncio
import socketio

loop = asyncio.get_event_loop()
sio = socketio.AsyncClient()


@sio.event
async def connect():
    print('Connection successful')
    await send_ping()


async def send_ping():
    print('ping is sent to server')
    await sio.emit(event='ping_pong_from_server')

@sio.event
def pong_from_server(data=None):  # Set a default value of None for the data argument
    if data:
        print(f'received pong from server with data: {data}')
    else:
        print('received pong from server (no data)')

async def main():
    await sio.connect('http://192.168.0.53:5000')
    await sio.wait()



if __name__ == '__main__':
    loop.run_until_complete(main())