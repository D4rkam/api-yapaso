from database import Base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship, Mapped


class User(Base):
    """
    User model for SQLAlchemy.
    """
    __tablename__ = "users"
    __allow_unmapped__ = True

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    name: Mapped[str] = Column(String(100), nullable=False)
    last_name: Mapped[str] = Column(String(100), nullable=False)
    username: Mapped[str] = Column(String(100), unique=True)
    hashed_password: Mapped[str] = Column(String(255))
    file_num: Mapped[int] = Column(Integer, nullable=False, unique=True)

    role: Mapped[str] = Column(String(10), default="user")

    balance: Mapped[int] = Column(Integer, default=0)

    orders: Mapped[list["Order"]] = relationship("Order", back_populates="user",  # type: ignore
                                                 cascade="all, delete-orphan")
