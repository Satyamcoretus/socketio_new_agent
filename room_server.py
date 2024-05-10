import socketio
import uuid
from socketio import AsyncNamespace
sio = socketio.AsyncServer(async_mode='asgi',logger=True)
app = socketio.ASGIApp(sio)

class ChatNamespace(AsyncNamespace):
    _room_id  = None
    _users = []
    async def on_connect(self,sid):
        # print('on_connect is triggered')
        # if auth:
        #     print(auth)
        # if environ:
        #     print(environ)
        # print(f'received sid {sid} from the client')

        await self.emit(event='message_on_client', data=f'connection successful at sid {sid}',namespace='/Chat')
        # first check if room exits
        if self._room_id:
            if sid not in self._users:
                self._users.append(sid)
        else:
            # create a room
            room_id = str(uuid.uuid4())         # Generate a unique room ID
            self._room_id = room_id

        response = {
            'sid': sid,
            'message': 'Welcome to the ChatROom !',
            'room_id': self._room_id
        }
        await self.emit(event='message_on_client', data=response,namespace='/Chat')
    async def on_join(self,sid,):
        self.enter_room(sid=sid,room=self._room_id,namespace='/Chat')
        response = {
            'sid' : sid,
            'message' : 'You have been added to the room',
            'room_id' : self._room_id
        }
        self.emit(event='message_on_client',data=response,namespace='/Chat')
    async def on_message(self,sid,data):
        # print(f"Message received from {sid}: {data}")
        if len(self._users) == 1:
            await self.emit(event='message_on_client', data=data, room=self._room_id,namespace='/Chat')
        else:
            await self.emit(event='message_on_client', data=data, room=self._room_id,skip_sid=sid,namespace='/Chat')

    async def on_disconnect(self, sid):

        print(f"Client disconnected: {sid}")
    async def on_disconnect(self, sid):
        self._users.clear()
        print(f"Client disconnected: {sid}")
        await self.emit(event='disconnect_message',data = 'ChatROom has been destroyed !',namespace='/Chat' )



sio.register_namespace(ChatNamespace('/Chat'))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app,host='192.168.0.53', port=8000)
