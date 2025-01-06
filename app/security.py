from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import joinedload

from app.config import get_settings
from app.dependencies.db import db_dependency

bcrypt_context = CryptContext(schemes=["bcrypt"])
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="api/auth/token")


async def get_current_user(db: db_dependency, token: str = Depends(oauth2_bearer)):
    from app.models.order_model import Order
    from app.models.user_model import User

    settings = get_settings()
    try:
        payload = jwt.decode(
            token,
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

        return user.__dict__
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo validar el usuario.",
        )


async def get_current_seller(db: db_dependency, token: str = Depends(oauth2_bearer)):
    from app.models.seller_model import Seller

    settings = get_settings()
    try:
        payload = jwt.decode(
            token,
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
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo validar el vendedor.",
        )
