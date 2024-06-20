from collections import defaultdict

from fastapi import WebSocket
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from websockets.exceptions import ConnectionClosedError


class NotificationManager:
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = defaultdict(list)

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id].append(websocket)

    async def broadcast(self, user_id: int, data: dict | BaseModel):
        data = jsonable_encoder(data)
        lost_connections = []
        for connection in self.active_connections[user_id]:
            try:
                await connection.send_json(data)
            except (RuntimeError, ConnectionClosedError):
                # https://github.com/tiangolo/fastapi/issues/3934
                # https://websockets.readthedocs.io/en/latest/howto/faq.html#what-does-connectionclosederror-no-close-frame-received-or-sent-mean
                # WS is already closed
                lost_connections.append(connection)
        # Removing connection on the go will result in skipped connection
        for connection in lost_connections:
            await self.disconnect(user_id, connection)

    async def disconnect(self, user_id: int, websocket: WebSocket):
        # Close the websocket
        try:
            await websocket.close()
        except (RuntimeError, ConnectionClosedError):
            # https://github.com/tiangolo/fastapi/issues/3934
            # https://websockets.readthedocs.io/en/latest/howto/faq.html#what-does-connectionclosederror-no-close-frame-received-or-sent-mean
            # Already closed
            pass

        # Remove the websocket from connections' list
        try:
            self.active_connections[user_id].remove(websocket)
        except ValueError:
            # Not in the list
            pass


notification_manager = NotificationManager()
