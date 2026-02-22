import base64
import hashlib
import logging
import secrets
from datetime import UTC, datetime, timedelta
from urllib.parse import urlencode

import httpx
from cryptography.fernet import Fernet
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.models.seller_model import Seller

logger = logging.getLogger(__name__)

MP_OAUTH_TOKEN_URL = "https://api.mercadopago.com/oauth/token"


def _get_fernet() -> Fernet:
    """Obtiene la instancia de Fernet con la clave configurada."""
    settings = get_settings()
    key = settings.FERNET_KEY.get_secret_value()
    if not key:
        raise HTTPException(
            status_code=500,
            detail="FERNET_KEY no está configurada en el servidor",
        )
    return Fernet(key.encode() if isinstance(key, str) else key)


def encrypt_token(token: str) -> str:
    """Encripta un token usando Fernet."""
    f = _get_fernet()
    return f.encrypt(token.encode()).decode()


def decrypt_token(encrypted_token: str) -> str:
    """Desencripta un token usando Fernet."""
    f = _get_fernet()
    return f.decrypt(encrypted_token.encode()).decode()


def _generate_code_verifier() -> str:
    """Genera un code_verifier aleatorio para PKCE (43-128 caracteres)."""
    return secrets.token_urlsafe(64)[:128]


def _generate_code_challenge(code_verifier: str) -> str:
    """Genera el code_challenge a partir del code_verifier usando S256."""
    digest = hashlib.sha256(code_verifier.encode()).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode()


def build_auth_url(seller_id: int, settings: Settings) -> tuple[str, str]:
    """Construye la URL de autorización de Mercado Pago con PKCE.
    Retorna (auth_url, code_verifier)."""
    code_verifier = _generate_code_verifier()
    code_challenge = _generate_code_challenge(code_verifier)

    params = {
        "response_type": "code",
        "client_id": settings.MP_CLIENT_ID,
        "redirect_uri": settings.MP_REDIRECT_URI,
        "state": str(seller_id),
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    auth_url = f"https://auth.mercadopago.com.ar/authorization?{urlencode(params)}"
    return auth_url, code_verifier


async def exchange_code_for_tokens(
    code: str, seller_id: int, code_verifier: str, db: Session, settings: Settings
) -> dict:
    """
    Intercambia el código de autorización de Mercado Pago por tokens.
    Guarda los tokens encriptados en la base de datos.
    """
    try:
        seller = db.query(Seller).filter(Seller.id == seller_id).first()
        if not seller:
            raise HTTPException(status_code=404, detail="Vendedor no encontrado")

        payload = {
            "client_id": settings.MP_CLIENT_ID,
            "client_secret": settings.MP_CLIENT_SECRET.get_secret_value(),
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": settings.MP_REDIRECT_URI,
            "code_verifier": code_verifier,
        }

        logger.info(f"Intercambiando code para seller_id={seller_id}")
        logger.info(f"redirect_uri={settings.MP_REDIRECT_URI}")
        logger.info(f"code_verifier length={len(code_verifier)}")

        async with httpx.AsyncClient() as client:
            response = await client.post(
                MP_OAUTH_TOKEN_URL,
                data=payload,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )

        logger.info(f"MP response status={response.status_code}")
        logger.info(f"MP response body={response.text}")

        if response.status_code != 200:
            detail = response.text
            try:
                detail = response.json()
            except Exception:
                pass
            raise HTTPException(
                status_code=400,
                detail=f"Error al obtener tokens de Mercado Pago: {detail}",
            )

        data = response.json()

        # Guardar tokens encriptados
        seller.mp_access_token = encrypt_token(data["access_token"])
        seller.mp_refresh_token = encrypt_token(data["refresh_token"])
        seller.mp_user_id = data["user_id"]
        seller.mp_token_expiration = datetime.now(UTC) + timedelta(
            seconds=data.get("expires_in", 15552000)
        )

        db.commit()
        logger.info(
            f"Tokens guardados para seller_id={seller_id}, mp_user_id={data['user_id']}"
        )

        return {
            "message": "Cuenta de Mercado Pago vinculada exitosamente",
            "mp_user_id": data["user_id"],
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error inesperado en exchange_code_for_tokens: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


async def unlink_mp_account(seller: Seller, db: Session) -> None:
    """
    Desvincula la cuenta de Mercado Pago del vendedor.

    NOTA: La API de Mercado Pago NO expone un endpoint público para revocar
    grants OAuth programáticamente. Los grant_type válidos en /oauth/token son
    únicamente: authorization_code, refresh_token y client_credentials.

    La revocación en MP ocurre cuando:
    - El token expira (180 días).
    - El vendedor revoca la autorización desde su cuenta de MP.
    - El vendedor cambia su contraseña en MP.

    Por lo tanto, al desvincular desde nuestra app, solo limpiamos los datos
    locales. Si el vendedor revoca desde MP, el webhook /mp/webhooks captura
    la notificación y sincroniza el estado.
    """
    if not seller.mp_access_token:
        raise HTTPException(
            status_code=400,
            detail="El vendedor no tiene una cuenta de Mercado Pago vinculada",
        )

    # Limpiar datos locales sin importar si MP respondió OK
    seller.mp_access_token = None
    seller.mp_refresh_token = None
    seller.mp_user_id = None
    seller.mp_token_expiration = None
    db.commit()

    logger.info(f"Cuenta de MP desvinculada para seller_id={seller.id}")


async def unlink_mp_account_by_mp_user_id(mp_user_id: int, db: Session) -> int | None:
    """
    Desvincula la cuenta de MP a partir del mp_user_id.
    Usado cuando MP notifica la revocación del grant.
    Retorna el seller_id si se encontró, None si no.
    """
    seller = db.query(Seller).filter(Seller.mp_user_id == mp_user_id).first()
    if not seller:
        logger.warning(
            f"Notificación de revocación de MP para mp_user_id={mp_user_id} "
            "pero no se encontró un vendedor asociado"
        )
        return None

    seller_id = seller.id
    seller.mp_access_token = None
    seller.mp_refresh_token = None
    seller.mp_user_id = None
    seller.mp_token_expiration = None
    db.commit()

    logger.info(
        f"Cuenta de MP desvinculada por webhook para seller_id={seller_id}, "
        f"mp_user_id={mp_user_id}"
    )
    return seller_id


async def refresh_mp_token(seller: Seller, db: Session, settings: Settings) -> str:
    """
    Renueva el access_token de MP usando el refresh_token almacenado.
    Devuelve el nuevo access_token ya desencriptado.
    """
    if not seller.mp_refresh_token:
        raise HTTPException(
            status_code=400,
            detail="El vendedor no tiene un refresh token de Mercado Pago",
        )

    payload = {
        "client_id": settings.MP_CLIENT_ID,
        "client_secret": settings.MP_CLIENT_SECRET.get_secret_value(),
        "grant_type": "refresh_token",
        "refresh_token": decrypt_token(seller.mp_refresh_token),
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            MP_OAUTH_TOKEN_URL,
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=400,
            detail="Error al renovar el token de Mercado Pago. El vendedor debe vincular nuevamente.",
        )

    data = response.json()

    seller.mp_access_token = encrypt_token(data["access_token"])
    seller.mp_refresh_token = encrypt_token(data["refresh_token"])
    seller.mp_token_expiration = datetime.now(UTC) + timedelta(
        seconds=data.get("expires_in", 15552000)
    )

    db.commit()

    return data["access_token"]
