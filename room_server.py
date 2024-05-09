import uvicorn
from fastapi import FastAPI
from fastapi.responses import  HTMLResponse
import socketio
import uuid

fast_api = FastAPI()
sio = socketio.AsyncServer(cors_allowed_origins='*',async_mode='asgi')
app = socketio.ASGIApp(sio,other_asgi_app=fast_api)


# html file
html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple Chatbot</title>
    <style>
        .chatbox {
            border: 1px solid #ddd;
            padding: 10px;
            height: 400px;
            overflow-y: scroll;
        }

        .chat-message {
            margin-bottom: 10px;
        }

        .user-message {
            text-align: right;
            font-weight: bold;
        }

        .bot-message {
            text-align: left;
        }
    </style>
</head>
<body>
    <div class="chatbox" id="chat-box">
    </div>
    <input type="text" id="message-input" placeholder="Type your message...">
    <button id="send-button">Send</button>

    <script src="https://cdn.socket.io/4/socket.io.min.js"></script>
    <script>
        const chatBox = document.getElementById('chat-box');
        const messageInput = document.getElementById('message-input');
        const sendButton = document.getElementById('send-button');
        const socket = io();  // Connect to the Socket.IO server

        // Function to create a chat message element
        function createChatMessage(message, isUserMessage) {
          const chatMessage = document.createElement('div');
          chatMessage.classList.add('chat-message');

          if (isUserMessage) {
            chatMessage.classList.add('user-message');
          } else {
            chatMessage.classList.add('bot-message');
          }

          chatMessage.textContent = message;
          return chatMessage;
        }

        // Function to simulate a bot response (replace with actual logic later)
        function simulateBotResponse(message) {
          const response = `You said: "${message}"`;
          const botMessage = createChatMessage(response, false);
          chatBox.appendChild(botMessage);
          chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
        }

        // Handle sending messages
        sendButton.addEventListener('click', () => {
          const userMessage = messageInput.value.trim();
          if (userMessage) {
            // Emit the "create_room" event with the user message (optional)
            socket.emit('create_room', userMessage);  // Trigger the event
            const userChatMessage = createChatMessage(userMessage, true);
            chatBox.appendChild(userChatMessage);
            messageInput.value = ''; // Clear the input field
          }
        });
    </script>
</body>
</html>

"""


@fast_api.get('/home',response_class=HTMLResponse)
async def home_page():
    return HTMLResponse(html)


rooms = {}  # Dictionary to store room information (clients in each room)

@sio.event
async def connect(sid):
    print(f'Client {sid} connected')

@sio.event
async def create_room(sid):
    room_id = str(uuid.uuid4())  # Generate a unique room ID
    rooms[room_id] = {sid}  # Add the connecting client to the room
    await sio.emit(event='room_created', data={'room_id': room_id}, to=sid)
    print(f'Client {sid} created room: {room_id}')

@sio.event
async def join_room(sid, room_id):
    if room_id in rooms:
        rooms[room_id].add(sid)  # Add client to the room
        await sio.emit(event='room_joined', data={'room_id': room_id}, to=sid)
        print(f'Client {sid} joined room: {room_id}')
        # Broadcast a message to existing clients in the room
        await sio.emit(event='user_joined', data={'message': f'{sid} has joined the room'}, room=room_id)
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

@sio.event
async def disconnect(sid):
    # Remove the client from any rooms they were in
    for room_id, clients in rooms.items():
        if sid in clients:
            clients.remove(sid)
            if not clients:  # If the room becomes empty, remove it
                del rooms[room_id]
            # Notify remaining clients in the room about the disconnection
            await sio.emit(event='user_left', data={'message': f'{sid} has left the room'}, room=room_id)
            print(f'Client {sid} disconnected from room: {room_id}')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('room_server:app', host='192.168.0.53', port=8000, reload=True)
