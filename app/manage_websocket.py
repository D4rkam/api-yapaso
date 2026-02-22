import asyncio
import json
import logging
from typing import Any

from fastapi import WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)


class WebSocketManager:
    """
    Gestor centralizado de conexiones WebSocket.

    Cada seller puede tener múltiples conexiones activas (varias pestañas/dispositivos).
    Los mensajes se envían como JSON con el formato:
    {
        "event": "nombre_del_evento",
        "data": { ... }
    }
    """

    def __init__(self):
        # seller_id -> lista de conexiones WebSocket activas
        self.active_connections: dict[int, list[WebSocket]] = {}
        self._heartbeat_interval: int = 30  # segundos

    @property
    def total_connections(self) -> int:
        return sum(len(conns) for conns in self.active_connections.values())

    async def connect(self, ws: WebSocket, seller_id: int) -> None:
        """Acepta y registra una nueva conexión WebSocket."""
        await ws.accept()
        if seller_id not in self.active_connections:
            self.active_connections[seller_id] = []
        self.active_connections[seller_id].append(ws)
        logger.info(
            f"WS conectado: seller_id={seller_id} "
            f"(conexiones activas: {self.total_connections})"
        )

    def disconnect(self, ws: WebSocket, seller_id: int) -> None:
        """Elimina una conexión WebSocket del registro."""
        if seller_id in self.active_connections:
            try:
                self.active_connections[seller_id].remove(ws)
            except ValueError:
                pass
            if not self.active_connections[seller_id]:
                del self.active_connections[seller_id]
        logger.info(
            f"WS desconectado: seller_id={seller_id} "
            f"(conexiones activas: {self.total_connections})"
        )

    def is_connected(self, seller_id: int) -> bool:
        """Verifica si un seller tiene conexiones activas."""
        return (
            seller_id in self.active_connections
            and len(self.active_connections[seller_id]) > 0
        )

    async def send_event(
        self, seller_id: int, event: str, data: dict[str, Any] | None = None
    ) -> None:
        """
        Envía un evento a todas las conexiones activas de un seller.

        Args:
            seller_id: ID del seller destinatario.
            event: Nombre del evento (ej: "mp_unlinked", "new_order").
            data: Datos adicionales del evento.
        """
        if not self.is_connected(seller_id):
            logger.debug(
                f"WS send_event ignorado: seller_id={seller_id} no tiene conexiones"
            )
            return

        message = json.dumps({"event": event, "data": data or {}})
        dead_connections: list[WebSocket] = []

        for ws in self.active_connections[seller_id]:
            try:
                await ws.send_text(message)
            except Exception as e:
                logger.warning(f"WS error al enviar a seller_id={seller_id}: {e}")
                dead_connections.append(ws)

        # Limpiar conexiones muertas
        for ws in dead_connections:
            self.disconnect(ws, seller_id)

    async def broadcast(self, event: str, data: dict[str, Any] | None = None) -> None:
        """Envía un evento a todos los sellers conectados."""
        for seller_id in list(self.active_connections.keys()):
            await self.send_event(seller_id, event, data)

    async def handle_connection(self, ws: WebSocket, seller_id: int) -> None:
        """
        Loop principal de una conexión WebSocket.
        Mantiene la conexión viva y escucha mensajes del client.

        Si no recibe ningún mensaje (ni ping) en 60 segundos,
        asume que la conexión murió y la cierra.
        El frontend DEBE enviar "ping" cada 25s para mantenerla.
        """
        await self.connect(ws, seller_id)
        try:
            while True:
                try:
                    # Timeout de 60s — si el client no manda ni un ping, cerramos
                    data = await asyncio.wait_for(ws.receive_text(), timeout=60.0)
                except asyncio.TimeoutError:
                    logger.info(
                        f"WS timeout: seller_id={seller_id} sin actividad por 60s"
                    )
                    await ws.close(code=1000, reason="Inactividad")
                    break

                # El client envía pings para mantener la conexión
                if data == "ping":
                    await ws.send_text(json.dumps({"event": "pong", "data": {}}))
        except WebSocketDisconnect:
            pass
        except Exception as e:
            logger.error(f"WS error inesperado seller_id={seller_id}: {e}")
        finally:
            self.disconnect(ws, seller_id)


# Instancia global — importar desde acá en toda la app
ws_manager = WebSocketManager()
