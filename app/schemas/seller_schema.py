from pydantic import BaseModel
from typing import List
from schemas.order_schema import Order
from schemas.product_schema import Product
from schemas.token_schema import Token


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
    # access_token_mp: str
    # refresh_token_mp: str
    orders: List[Order]
    products: List[Product]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class SellerDataToken(Seller):
    token: Token
