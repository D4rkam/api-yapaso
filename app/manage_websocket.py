from fastapi import WebSocket
from typing import Dict
import json


class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, seller_id: int):
        await websocket.accept()
        self.active_connections[seller_id] = websocket

    def disconnect(self, seller_id: int):
        if seller_id in self.active_connections:
            del self.active_connections[seller_id]

    async def send_new_order(self, seller_id: int, order_data: dict):
        if seller_id in self.active_connections:
            ws = self.active_connections[seller_id]
            await ws.send_text(json.dumps(order_data))

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = WebSocketManager()
