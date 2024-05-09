import socketio

client = socketio.AsyncClient()





@client.event
async def receiver_from_server(data):
    if data:
        print('received data from server')
        print(data)



async def main():
    await client.connect('http://localhost:8001')
    await client.emit(event='connect')
    while True:
        input_message = input('Enter the input')
        await client.emit(event='communication_channel',data=input_message)



if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
