from pydantic import BaseModel
from typing import List
from .product_schema import ProductForOrder, Product


# TODO: cambiar el esquema, adaptando los productos

class OrderBase(BaseModel):
    user_id: int
    products: List[ProductForOrder]


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: int
    products: List[Product]

    class Config:
        from_attributes = True
