from database import Base
from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, backref
from .user_model import User


order_products = Table(
    'order_products',
    Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id')),
    Column('product_id', Integer, ForeignKey('products.id'))
)


class Order(Base):
    """
    Order model for SQLAlchemy.
    """
    __tablename__ = "orders"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = Column(
        Integer, ForeignKey("users.id"), nullable=False)

    user: Mapped[User] = relationship("User", back_populates="orders")

    products = relationship(
        "Product", secondary=order_products, back_populates="orders"
    )
