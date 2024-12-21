from sqlalchemy.orm import Session
from app.models.seller_model import Seller


def get_seller_by_email(db: Session, email: str):
    return db.query(Seller).filter(Seller.email == email).first()


def get_seller_by_id(db: Session, seller_id: int):
    return db.query(Seller).filter(Seller.id == seller_id).first()
