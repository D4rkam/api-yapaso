from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, relationship

from app.database import Base


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
        "Order", back_populates="seller"
    )
    products: Mapped[list["Product"]] = relationship(  # type: ignore
        "Product", back_populates="seller"
    )

    notifications: Mapped[list["Notification"]] = relationship(
        "Notification", back_populates="seller", cascade="all, delete-orphan"
    )

    @property
    def mp_linked(self) -> bool:
        """True si el vendedor vinculó su cuenta de Mercado Pago."""
        return self.mp_access_token is not None and self.mp_access_token != ""
