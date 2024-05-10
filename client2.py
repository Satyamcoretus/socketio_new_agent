import time

import socketio

client = socketio.AsyncClient()


@client.event
async def receiver_from_server(data=None):
    if data:
        print('received data from server')
        print(data)
    else:
        print('NO data is received from server side event ')


async def get_input():
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, input, "Enter a message to send to the server: ")



async def main():
    await client.connect('http://localhost:8001')

    while True:
        message_to_send = await get_input()

        # Send the message to the server
        await client.emit(event='communication_channel',data =  message_to_send)

        await asyncio.sleep(0.5)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
