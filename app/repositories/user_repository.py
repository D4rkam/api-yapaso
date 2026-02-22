from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.user_model import User


class UserRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.db_session.query(User).offset(skip).limit(limit).all()

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.db_session.query(User).filter(User.id == user_id).first()

    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.db_session.query(User).filter(User.username == username).first()

    def get_user_by_file_num(self, file_num_user: int) -> Optional[User]:
        return (
            self.db_session.query(User).filter(User.file_num == file_num_user).first()
        )

    def add_user(self, user: User) -> User:
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user

    def update_user(self, user: User) -> User:
        self.db_session.merge(user)
        self.db_session.commit()
        return user

    def delete_user(self, user_id: int) -> None:
        user = self.get_user_by_id(user_id)
        if user:
            self.db_session.delete(user)
            self.db_session.commit()
            self.db_session.delete(user)
            self.db_session.commit()
