from fastapi import APIRouter, HTTPException, status
from dependencies import db_dependency, user_dependency
from typing import List
from schemas.user_schema import User
from services.user_service import get_users


router = APIRouter(
    prefix="/users",
    tags=["Usuarios"]
)


@router.get("/", status_code=status.HTTP_200_OK)
async def user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Fallo la autenticación")
    return {"User": user}


@router.get("/all", response_model=List[User])
async def users(db: db_dependency, user: user_dependency):
    return get_users(db)
