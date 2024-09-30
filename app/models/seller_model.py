from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from .order_model import Order
from .product_model import Product


class Seller(Base):
    """
    Seller model for SQLAlchemy.
    """
    __tablename__ = "sellers"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), index=True)
    password = Column(String(255), index=True)
    name_store = Column(String(100), index=True)
    school_name = Column(String(100), index=True)
    location = Column(String(100), index=True)
    access_token = Column(String(255), index=True, nullable=True)
    refresh_token = Column(String(255), index=True, nullable=True)

    orders: Mapped[list[Order]] = relationship(
        "Order", back_populates="seller")
    products: Mapped[list[Product]] = relationship(
        "Product", back_populates="seller")
