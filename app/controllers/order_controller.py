from fastapi import APIRouter
from fastapi import status
from typing import List
from app.dependencies import db_dependency, user_dependency, seller_dependency
from app.schemas.order_schema import OrderCreate, Order
from app.services.order_service import create_user_order, get_orders
from app.security import verify_roles
from app.models.user_model import User
from fastapi import Depends


router = APIRouter(
    prefix="/order",
    tags=["Pedidos"]
)


@router.post("/", status_code=status.HTTP_200_OK)
async def create_order_for_user(order: OrderCreate, db: db_dependency, current_user: user_dependency):
    return create_user_order(db=db, order=order)


@router.get("/", response_model=List[Order])
async def get_orders_for_seller(db: db_dependency, current_user: seller_dependency):
    return get_orders(db)
