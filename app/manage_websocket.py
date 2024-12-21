from fastapi import WebSocket
from typing import Dict
import json


class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, ws: WebSocket, seller_id: int):
        await ws.accept()
        if seller_id not in self.active_connections:
            self.active_connections[seller_id] = []
        self.active_connections[seller_id].append(ws)

    def disconnect(self, seller_id: int, ws: WebSocket):
        if seller_id in self.active_connections:
            self.active_connections[seller_id].remove(ws)
            if not self.active_connections[seller_id]:
                del self.active_connections[seller_id]

    async def send_to_seller(self, seller_id: int, message: str):
        if seller_id in self.active_connections:
            for connection in self.active_connections[seller_id]:
                await connection.send_text(json.dumps(message))


manager = WebSocketManager()
