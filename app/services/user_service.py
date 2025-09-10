from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user_model import User
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.user_repository = UserRepository(db_session)

    def get_user_by_id(self, user_id: int) -> User:
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def get_user_by_username(self, username: str) -> User:
        user = self.user_repository.get_user_by_username(username)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def verify_user_by_username_filenum(self, username: str, filenum: int) -> User:
        user = self.user_repository.get_user_by_username(username)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.file_num != filenum:
            raise HTTPException(status_code=400, detail="User not found")

        return user

    def get_user_by_file_num(self, file_num_user: int) -> User:
        user = self.user_repository.get_user_by_file_num(file_num_user)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def get_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        users = self.user_repository.get_all_users(skip=skip, limit=limit)
        return users

    def add_balance(self, mount: float, user_id: int):
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.balance += mount

        self.db.commit()
        self.db.refresh(user)

        return user.balance

    def substract_balance(self, mount: float, user_id: int):
        user = self.user_repository.get_user_by_id(user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.balance - mount >= 0:
            user.balance -= mount
        else:
            raise HTTPException(
                status_code=500, detail="El saldo no puede ser negativo"
            )

        self.db.commit()
        self.db.refresh(user)
        return user.balance
