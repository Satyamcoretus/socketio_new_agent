import socketio

client = socketio.AsyncClient()



@client.event
async def connect():
    print('connection is established')


# @client.event
# async def communication_channel():


async def main():
    await client.connect('http://localhost:8001')
    await connect()





if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
