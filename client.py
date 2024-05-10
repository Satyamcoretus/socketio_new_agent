import socketio

# Create a Socket.IO client instance
client = socketio.AsyncClient()

# Define event handlers
@client.event
def connect():
    print('Connected to server')

@client.event
def communication(message):
    print(f'message is received - {message}')

async def main():
    await client.connect('http://localhost:8001')

    while True:
        input_message = await input('Enter client message (or "exit" to quit): ')
        await client.emit(event='communication', data=input_message)
        if input_message == 'exit':
            break

    await client.disconnect()  # Gracefully disconnect

# Run the main function
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
