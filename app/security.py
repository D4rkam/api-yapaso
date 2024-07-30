from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session, joinedload
from models.order_model import Order
from database import SessionLocal
from config import settings
from models.user_model import User


bcrypt_context = CryptContext(schemes=["bcrypt"])
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="api/auth/token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)], db: db_dependency):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="No es un usuario valido.")
        user = db.query(User).options(joinedload(User.orders).joinedload(
            Order.products)).filter(User.id == user_id).first()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado.")

        return user
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="No se pudo validar el usuario.")
