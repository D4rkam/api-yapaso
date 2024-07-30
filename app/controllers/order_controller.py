from fastapi import APIRouter
from fastapi import status
from typing import List
from dependencies import db_dependency
from schemas.order_schema import OrderCreate, Order
from services.order_service import create_user_order, get_orders
from dependencies import user_dependency


router = APIRouter(
    prefix="/order",
    tags=["Pedidos"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order_for_user(order: OrderCreate, db: db_dependency, current_user: user_dependency):
    return create_user_order(db=db, order=order, user_id=current_user.id)


@router.get("/", response_model=List[Order])
async def get_orders_user(db: db_dependency, user: user_dependency):
    return get_orders(db)
