from datetime import UTC, datetime, timedelta

from fastapi import HTTPException
from jose import jwt
from sqlalchemy.orm import Session

from app.dependencies.settings import settings_dependency
from app.models.seller_model import Seller
from app.models.user_model import User
from app.security import bcrypt_context


def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def authenticate_seller(email: str, password: str, db: Session):
    seller = db.query(Seller).filter(Seller.email == email).first()
    if not seller:
        return False
    if not bcrypt_context.verify(password, seller.hashed_password):
        return False
    return seller


def create_access_token(
    username: str, user_id: int, expires_delta: timedelta, settings: settings_dependency
):
    encode = {"sub": username, "id": user_id}
    expires = datetime.now(UTC) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(
        encode, settings.SECRET_KEY.get_secret_value(), algorithm=settings.ALGORITHM
    )


def create_access_token_seller(
    email: str, seller_id: int, expires_delta: timedelta, settings: settings_dependency
):
    encode = {"sub": email, "id": seller_id}
    expires = datetime.now(UTC) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(
        encode, settings.SECRET_KEY.get_secret_value(), algorithm=settings.ALGORITHM
    )


def create_refresh_token(
    sub: str, sub_id: int, settings: settings_dependency, is_seller: bool = False
) -> str:
    expires = datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    encode = {"sub": sub, "id": sub_id, "exp": expires}
    return jwt.encode(
        encode,
        settings.REFRESH_SECRET_KEY.get_secret_value(),
        algorithm=settings.ALGORITHM,
    )


def refresh_access_token(
    refresh_token: str, is_seller: bool = False, settings: settings_dependency = None
) -> str:
    payload = verify_token(
        refresh_token,
        settings.REFRESH_SECRET_KEY.get_secret_value(),
        settings.ALGORITHM,
    )
    if not payload:
        raise HTTPException(status_code=401, detail="Refresh token inválido")

    # Generar nuevo token de acceso basado en los datos del payload
    sub = payload.get("sub")
    sub_id = payload.get("id")
    if sub is None or sub_id is None:
        raise HTTPException(status_code=401, detail="Refresh token incompleto")

    if is_seller:
        new_token = create_access_token_seller(
            email=sub,
            seller_id=sub_id,
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            settings=settings,
        )
    else:
        new_token = create_access_token(
            username=sub,
            user_id=sub_id,
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            settings=settings,
        )
    return new_token


def verify_token(token: str, secret_key: str, algorithm: str):
    try:
        payload = jwt.decode(
            token,
            secret_key,
            algorithms=[algorithm],
        )
        return payload if payload.get("sub") else None
    except jwt.JWTError:
        return None
