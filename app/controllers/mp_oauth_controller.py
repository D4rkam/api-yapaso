from fastapi import APIRouter, status

from app.dependencies.db import db_dependency
from app.dependencies.security import seller_dependency
from app.dependencies.settings import settings_dependency
from app.schemas.mp_oauth_schema import (
    MPAuthURLResponse,
    MPOAuthCallbackRequest,
    MPOAuthTokenResponse,
)
from app.services.mp_oauth_service import build_auth_url, exchange_code_for_tokens

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
