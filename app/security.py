from fastapi import Cookie, HTTPException, status
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import joinedload

from app.config import get_settings
from app.dependencies.db import db_dependency

bcrypt_context = CryptContext(schemes=["bcrypt"])


async def get_current_user(
    db: db_dependency,
    session_token_user: str = Cookie(None),
):
    from app.models.order_model import Order
    from app.models.user_model import User

    settings = get_settings()

    if session_token_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se proporcionó el token de sesión del usuario.",
        )
    try:
        payload = jwt.decode(
            session_token_user,
            settings.SECRET_KEY.get_secret_value(),
            algorithms=[settings.ALGORITHM],
        )
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No es un usuario valido.",
            )
        user = (
            db.query(User)
            .options(joinedload(User.orders).joinedload(Order.products))
            .filter(User.id == user_id)
            .first()
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no encontrado.",
            )

        return user

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El token ha expirado.",
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo validar el usuario.",
        )


# Cambiar Oauth2PasswordBearer a un token en cookie para vendedores
async def get_current_seller(
    db: db_dependency, session_token_seller: str = Cookie(None)
):
    from app.models.seller_model import Seller

    if session_token_seller is None:
        print("No se proporcionó el token de sesión del vendedor.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se proporcionó el token de sesión del vendedor.",
        )

    settings = get_settings()
    try:
        payload = jwt.decode(
            session_token_seller,
            settings.SECRET_KEY.get_secret_value(),
            algorithms=[settings.ALGORITHM],
        )
        email: str = payload.get("sub")
        seller_id: int = payload.get("id")
        if email is None or seller_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No es un vendedor valido.",
            )
        seller = db.query(Seller).filter(Seller.id == seller_id).first()

        if seller is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Vendedor no encontrado.",
            )
        return seller
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El token del vendedor ha expirado.",
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo validar el vendedor.",
        )
