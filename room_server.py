import time
from Database.mongodb import Database
import socketio
import uuid
from socketio import AsyncNamespace
sio = socketio.AsyncServer(async_mode='asgi',logger=True)
app = socketio.ASGIApp(sio)


# @sio.event(namespace='/Chat')
# async def connect(sid):
#     # print('connect is triggered')
#     # if auth:
#     #     print('auth')
#     #     print(auth)
#     # if environ:
#     #     print('----------------------')
#     #     print('environ')
#     #     print(environ)
#     print(f'received sid {sid} from the client')


class ChatNamespace(AsyncNamespace):
    _room_id  = None
    _users = []
    _start_time = None
    async def on_create_room(self,sid):
        self._start_time = time.time()
        await self.emit(event='message_on_client', data=f'connection successful at sid {sid}',namespace='/Chat')
        # first check if room exits
        if self._room_id:
            if sid not in self._users:
                self._users.append(sid)
        else:
            # create a room
            room_id = str(uuid.uuid4())         # Generate a unique room ID
            self._room_id = room_id
            self._users.append(sid)

        response = {
            'sid': sid,
            'message': 'Welcome to the ChatROom !',
            'room_id': self._room_id
        }
        await self.emit(event='message_on_client', data=response,namespace='/Chat')
    async def on_join(self,sid,):
        await self.on_create_room(sid=sid)
        await self.enter_room(sid=sid,room=self._room_id,namespace='/Chat')
        response = {
            'sid' : sid,
            'message' : f'You have been added to the room [{self._room_id}]',
            'room_id' : self._room_id
        }
        await self.emit(event='message_on_client',data=response,namespace='/Chat')

    async def on_message(self,sid,data):

        await self.emit(event='message_on_client', data=data, room=self._room_id,namespace='/Chat',skip_sid=True)

    async def on_disconnect(self, sid):
        self._room_id = None
        self._users.clear()
        print(f"Client disconnected: {sid}")
        end_time = time.time()
        # if self._start_time is not None:
        #     total_time = end_time-self._start_time
        # # send time to mongodb of the chat
        # Database.initialize()
        # Database.update_agent_info(collection_name='Embeddings',time=total_time)
        # reset time
        self._start_time = None
        await self.emit(event='disconnect_message',data = 'ChatROom has been destroyed !',namespace='/Chat' ,room=self._room_id)


sio.register_namespace(ChatNamespace('/Chat'))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app,host='192.168.0.53', port=8000)
