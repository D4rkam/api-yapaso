from app.database import Base
from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, relationship


class Seller(Base):
    """
    Seller model for SQLAlchemy.
    """
    __tablename__ = "sellers"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), index=True)
    hashed_password = Column(String(255), index=True)
    name_store = Column(String(100), index=True)
    school_name = Column(String(100), index=True)
    location = Column(String(100), index=True)
    role = Column(String(10), default="seller")

    # Tokens de Mercado Pago (encriptados con Fernet)
    mp_access_token = Column(Text, nullable=True)
    mp_refresh_token = Column(Text, nullable=True)
    mp_user_id = Column(Integer, nullable=True)
    mp_token_expiration = Column(DateTime, nullable=True)

    orders: Mapped[list["Order"]] = relationship(  # type: ignore
        "Order", back_populates="seller")
    products: Mapped[list["Product"]] = relationship(  # type: ignore
        "Product", back_populates="seller")
