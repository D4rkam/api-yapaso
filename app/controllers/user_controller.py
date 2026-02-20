from fastapi import APIRouter, HTTPException, status

from app.dependencies.db import db_dependency
from app.dependencies.security import user_dependency
from app.services.user_service import UserService


class UserController:
    def __init__(self):
        self.router = APIRouter(prefix="/users", tags=["Usuarios"])
        self.router.add_api_route(
            "/",
            self.get_current_user,
            methods=["GET"],
            status_code=status.HTTP_200_OK,
        )
        self.router.add_api_route(
            "/{username}",
            self.user_by_username,
            methods=["GET"],
            status_code=status.HTTP_200_OK,
        )

    @staticmethod
    async def get_current_user(
        current_user: user_dependency,
    ):
        if current_user is None:
            raise HTTPException(status_code=401, detail="Fallo la autenticación")
        return {"User": current_user}

    @staticmethod
    async def user_by_username(
        db: db_dependency, username: str, current_user: user_dependency
    ):
        return UserService(db_session=db).get_user_by_username(username)
