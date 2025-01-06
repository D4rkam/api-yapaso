from datetime import datetime, timedelta

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
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(
        encode, settings.SECRET_KEY.get_secret_value(), algorithm=settings.ALGORITHM
    )


def create_access_token_seller(
    email: str, seller_id: int, expires_delta: timedelta, settings: settings_dependency
):
    encode = {"sub": email, "id": seller_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(
        encode, settings.SECRET_KEY.get_secret_value(), algorithm=settings.ALGORITHM
    )
