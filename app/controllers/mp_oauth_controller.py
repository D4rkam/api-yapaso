import logging

from fastapi import APIRouter, Request, status

from app.dependencies.db import db_dependency
from app.dependencies.security import seller_dependency
from app.dependencies.settings import settings_dependency
from app.manage_websocket import ws_manager
from app.repositories.notification_repository import create_notification
from app.schemas.mp_oauth_schema import (
    MPAuthURLResponse,
    MPOAuthCallbackRequest,
    MPOAuthTokenResponse,
    MPUnlinkResponse,
)
from app.services.mp_oauth_service import (
    build_auth_url,
    exchange_code_for_tokens,
    unlink_mp_account,
    unlink_mp_account_by_mp_user_id,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/mp", tags=["Mercado Pago OAuth"])


@router.get("/auth-url", response_model=MPAuthURLResponse)
async def get_mp_auth_url(
    current_seller: seller_dependency,
    settings: settings_dependency,
):
    """
    Genera la URL de autorización de Mercado Pago para el vendedor autenticado.
    El frontend redirige al vendedor a esta URL.
    """
    auth_url, code_verifier = build_auth_url(current_seller.id, settings)
    return MPAuthURLResponse(auth_url=auth_url, code_verifier=code_verifier)


@router.post(
    "/callback",
    response_model=MPOAuthTokenResponse,
    status_code=status.HTTP_201_CREATED,
)
async def mp_oauth_callback(
    callback_data: MPOAuthCallbackRequest,
    db: db_dependency,
    settings: settings_dependency,
):
    """
    Recibe el code de autorización de MP y lo intercambia por tokens.
    El frontend captura code y state de la URL de redirect y los envía aquí.
    """
    seller_id = int(callback_data.state)
    result = await exchange_code_for_tokens(
        code=callback_data.code,
        seller_id=seller_id,
        code_verifier=callback_data.code_verifier,
        db=db,
        settings=settings,
    )
    return MPOAuthTokenResponse(**result)


@router.delete("/unlink", response_model=MPUnlinkResponse)
async def mp_unlink(
    current_seller: seller_dependency,
    db: db_dependency,
):
    """
    Desvincula la cuenta de Mercado Pago del vendedor autenticado.
    Limpia todos los tokens y datos de MP almacenados.
    """
    await unlink_mp_account(current_seller, db)

    # Notificar al frontend por WebSocket
    await ws_manager.send_event(
        current_seller.id,
        "mp_unlinked",
        {"message": "Cuenta de Mercado Pago desvinculada"},
    )

    return MPUnlinkResponse(message="Cuenta de Mercado Pago desvinculada exitosamente")


@router.post("/webhooks", status_code=status.HTTP_200_OK)
async def mp_webhook(
    request: Request,
    db: db_dependency,
):
    """
    Recibe notificaciones Webhook de Mercado Pago (tópico mp-connect).

    MP envía los datos como query parameters:
    POST /api/mp/webhooks?data.id=123456&type=mp-connect

    Y opcionalmente un JSON body con más detalles:
    {
        "id": 12345,
        "live_mode": true,
        "type": "mp-connect",
        "action": "application.deauthorized",
        "user_id": 44444,
        "data": { "id": "999999999" }
    }
    """
    # Leer datos de query params (siempre presentes)
    query_params = dict(request.query_params)
    notification_type = query_params.get("type")
    data_id = query_params.get("data.id")

    # Intentar leer JSON body para datos adicionales (action, user_id)
    action = None
    mp_user_id = None
    try:
        body = await request.json()
        action = body.get("action")
        mp_user_id = body.get("user_id")
        notification_type = notification_type or body.get("type")
        data_id = data_id or str(body.get("data", {}).get("id", ""))
    except Exception:
        pass

    logger.info(
        f"Webhook recibido: type={notification_type}, action={action}, "
        f"user_id={mp_user_id}, data.id={data_id}, "
        f"query_params={query_params}"
    )

    # MP envía type="mp-connect" cuando el vendedor vincula/desvincula
    if notification_type == "mp-connect":
        # Si tenemos action del body, usamos eso para mayor precisión
        if action == "application.deauthorized" and mp_user_id:
            seller_id = await unlink_mp_account_by_mp_user_id(int(mp_user_id), db)
            if seller_id:
                create_notification(db, seller_id, "mp_unlinked", {
                    "message": "Cuenta de Mercado Pago desvinculada desde MP",
                    "source": "webhook"
                })
                await ws_manager.send_event(
                    seller_id,
                    "mp_unlinked",
                    {
                        "message": "Cuenta de Mercado Pago desvinculada desde MP",
                        "source": "webhook",
                    },
                )
            logger.info(
                f"Desvinculación procesada por webhook para mp_user_id={mp_user_id}"
            )
        elif action == "application.deauthorized" and data_id:
            # Fallback: usar data.id como mp_user_id
            seller_id = await unlink_mp_account_by_mp_user_id(int(data_id), db)
            if seller_id:
                create_notification(db, seller_id, "mp_unlinked", {
                    "message": "Cuenta de Mercado Pago desvinculada desde MP",
                    "source": "webhook"
                })
                await ws_manager.send_event(
                    seller_id,
                    "mp_unlinked",
                    {
                        "message": "Cuenta de Mercado Pago desvinculada desde MP",
                        "source": "webhook",
                    },
                )
            logger.info(
                f"Desvinculación procesada por webhook (data.id) para mp_user_id={data_id}"
            )
        elif action == "application.authorized":
            logger.info(
                f"Vinculación detectada por webhook para user_id={mp_user_id or data_id}"
            )
        elif not action and data_id:
            # Solo query params sin body: no podemos distinguir autorización
            # de desautorización. Verificamos si el token del seller sigue válido.
            logger.warning(
                f"Notificación mp-connect sin action. data.id={data_id}. "
                "No se puede determinar si es vinculación o desvinculación."
            )

    # MP espera un 200 para confirmar recepción
    return {"status": "ok"}
