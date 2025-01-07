from fastapi import APIRouter, HTTPException, status

from app.dependencies.db import db_dependency
from app.dependencies.security import user_dependency
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Usuarios"])


@router.get("/", status_code=status.HTTP_200_OK)
async def user(current_user: user_dependency):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Fallo la autenticación")

    return {"User": current_user}


@router.get("/{username}")
async def user_for_username(
    db: db_dependency, username: str, current_user: user_dependency
):
    return UserService.get_user_by_username(username)
