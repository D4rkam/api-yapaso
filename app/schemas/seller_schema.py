from typing import List

from pydantic import BaseModel

from app.schemas.order_schema import Order
from app.schemas.product_schema import Product


class LoginSellerRequest(BaseModel):
    email: str
    password: str


class CreateSellerRequest(LoginSellerRequest):
    email: str
    password: str
    name_store: str
    school_name: str
    location: str


class Seller(CreateSellerRequest):
    """
    Seller schema for SQLAlchemy.
    """

    id: int
    orders: List[Order]
    products: List[Product]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
