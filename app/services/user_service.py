from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user_model import User


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def verify_user_by_username_filenum(db: Session, username: str, filenum: int):
    return db.query(User).filter(User.username == username and User.file_num == filenum).first()


def get_user_by_file_num(db: Session, file_num_user: int):
    return db.query(User).filter(User.file_num == file_num_user).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def add_balance(db: Session, mount: float, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.balance += mount

    db.commit()
    db.refresh(user)

    return user.balance


def substract_balance(db: Session, mount: float, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.balance - mount >= 0:
        user.balance -= mount
    else:
        raise HTTPException(
            status_code=500, detail="El saldo no puede ser negativo")

    db.commit()
    db.refresh(user)
    return user.balance
