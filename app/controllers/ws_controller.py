import logging
from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Query, WebSocket, status
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError

from app.config import get_settings
from app.dependencies.security import seller_dependency
from app.dependencies.settings import settings_dependency
from app.manage_websocket import ws_manager

logger = logging.getLogger(__name__)

router = APIRouter(tags=["WebSocket"])

WS_TICKET_EXPIRE_SECONDS = 30


@router.get("/ws/ticket")
async def get_ws_ticket(
    current_seller: seller_dependency,
    settings: settings_dependency,
):
    """
    Genera un ticket JWT de corta duración (30s) para autenticar la conexión WS.

    Flujo:
    1. Frontend llama GET /api/ws/ticket (la cookie httpOnly viaja automáticamente)
    2. Recibe {"ticket": "<jwt>"}
    3. Conecta a ws://host/api/ws/seller?ticket=<jwt>
    """
    payload = {
        "sub": current_seller.email,
        "id": current_seller.id,
        "purpose": "ws_ticket",
        "exp": datetime.now(UTC) + timedelta(seconds=WS_TICKET_EXPIRE_SECONDS),
    }
    ticket = jwt.encode(
        payload,
        settings.SECRET_KEY.get_secret_value(),
        algorithm=settings.ALGORITHM,
    )
    return {"ticket": ticket}


async def _authenticate_seller_ws(ticket: str) -> int | None:
    """
    Valida un ticket JWT de corta duración para WebSocket.
    Retorna el seller_id o None si es inválido/expirado.
    """
    if not ticket:
        return None

    settings = get_settings()
    try:
        payload = jwt.decode(
            ticket,
            settings.SECRET_KEY.get_secret_value(),
            algorithms=[settings.ALGORITHM],
        )
        # Verificar que es un ticket de WS (no un token de sesión reutilizado)
        if payload.get("purpose") != "ws_ticket":
            logger.warning("WS: ticket con purpose inválido")
            return None

        seller_id: int | None = payload.get("id")
        email: str | None = payload.get("sub")
        if seller_id is None or email is None:
            return None
        return seller_id
    except ExpiredSignatureError:
        logger.warning("WS: ticket expirado")
        return None
    except JWTError:
        logger.warning("WS: ticket inválido")
        return None


@router.websocket("/ws/seller")
async def seller_websocket(
    ws: WebSocket,
    ticket: str = Query(...),
):
    """
    Endpoint WebSocket para sellers.

    El frontend se conecta pasando un ticket temporal como query param:
    ws://host/api/ws/seller?ticket=<ticket_jwt>

    El ticket se obtiene previamente con GET /api/ws/ticket.

    Eventos que el server puede enviar:
    - mp_unlinked: la cuenta de MP fue desvinculada
    - mp_linked: la cuenta de MP fue vinculada
    - new_order: nueva orden recibida
    - order_updated: orden actualizada
    """
    seller_id = await _authenticate_seller_ws(ticket)
    if seller_id is None:
        await ws.close(code=status.WS_1008_POLICY_VIOLATION, reason="Ticket inválido")
        return

    await ws_manager.handle_connection(ws, seller_id)
