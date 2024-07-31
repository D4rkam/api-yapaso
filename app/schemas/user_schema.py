from pydantic import BaseModel
from typing import List, Optional
from schemas.order_schema import Order
from schemas.token_schema import Token


class CreateUserRequest(BaseModel):
    name: str
    last_name: str
    username: str
    password: str
    file_num: str

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class UserLogin(BaseModel):
    username: str
    password: str


class User(CreateUserRequest):
    id: int
    orders: List[Order]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class UserDataToken(User):
    token: Token


class ResponseUserDataToken(BaseModel):
    user: UserDataToken
