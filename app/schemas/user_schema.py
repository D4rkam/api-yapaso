from pydantic import BaseModel
from typing import List, Optional
from app.schemas.order_schema import Order
from app.schemas.token_schema import Token


class CreateUserRequest(BaseModel):
    name: str
    last_name: str
    username: str
    password: str
    file_num: str
    # balance: float = 0

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class UserLogin(BaseModel):
    username: str
    password: str


class User(CreateUserRequest):
    id: int
    orders: List[Order]
    balance: int
    role: str

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class UserDataToken(User):
    token: Token


class ResponseUserDataToken(BaseModel):
    user: UserDataToken
