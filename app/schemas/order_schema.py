from pydantic import BaseModel
from typing import List
from .product_schema import ProductForOrder, Product
from datetime import datetime


# TODO: cambiar el esquema, adaptando los productos

class OrderBase(BaseModel):
    user_id: int
    seller_id: int
    products: List[ProductForOrder]


class OrderCreate(OrderBase):
    datetime_order: str


class Order(OrderBase):
    id: int
    products: List[Product]
    total: float = 0
    status: str = "ENCARGADO"

    # Fecha y hora del pedido
    created_at: datetime

    # Fecha y hora seleccionada del usuario
    datetime_order: datetime

    class Config:
        from_attributes = True
