from sqlalchemy.orm import Session
from database import SessionLocal
from typing import Annotated
from fastapi import Depends
from security import get_current_user, get_current_seller


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
seller_dependency = Annotated[dict, Depends(get_current_seller)]
