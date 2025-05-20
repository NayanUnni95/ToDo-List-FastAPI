from fastapi import WebSocket, WebSocketDisconnect
from typing import List
from datetime import datetime
from ..services.Oauth2 import verify_token_valid_or_invalid


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        for connection in self.active_connections:
            if connection == websocket:
                self.active_connections.remove(connection)

    async def send_personal_msg(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, user: str, websocket: WebSocket):
        response_data = {
            "generated_time": str(datetime.now()),
            "active_connections": len(self.active_connections),
            "sender": user,
            "message": message,
        }
        for connection in self.active_connections:
            if connection != websocket:
                await connection.send_json(response_data)


manager = ConnectionManager()


async def websocket_connection(token: str, websocket: WebSocket):
    user = verify_token_valid_or_invalid(token=token)
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data, user, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"{user} left the room")
