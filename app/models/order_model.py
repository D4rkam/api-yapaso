from app.database import Base
from sqlalchemy import Column, Integer, ForeignKey, Table, Float, String, DateTime
from sqlalchemy.orm import relationship, Mapped, backref
from app.models.user_model import User
from datetime import datetime

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
    products: Mapped[list["Product"]] = relationship(  # type: ignore
        "Product", secondary=order_products, back_populates="orders"
    )
    status: Mapped[str] = Column(
        String(25), nullable=False, default="ENCARGADO")
    datetime_order: Mapped[datetime] = Column(DateTime, nullable=False)
    total: Mapped[float] = Column(Float, nullable=False, default=0)

    seller_id: Mapped[int] = Column(Integer, ForeignKey("sellers.id"))
    seller: Mapped["Seller"] = relationship(  # type: ignore
        "Seller", back_populates="orders")

    created_at: Mapped[datetime] = Column(
        DateTime, default=datetime.now, nullable=False)


""" TODO: ESTOY IMPLEMENTANDO LOS DATOS FALTANTES EN UN PEDIDO
    - Estado del pedido -> ENCARGADO: cuando se crea el pedido | ENTREGADO: cuando se entrega el pedido | CANCELADO: cuando se cancela el pedido
    - Fecha y Hora de entrega -> lo establece el usuario
    - Fecha de pedido -> datetime.now() lo establece el sistema
    - Total -> lo establece el sistema cuando se realiza la suma de los productos
"""
