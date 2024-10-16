from fastapi import APIRouter
from fastapi import status
from typing import List
from dependencies import db_dependency
from schemas.order_schema import OrderCreate, Order
from services.order_service import create_user_order, get_orders
from security import verify_roles
from models.user_model import User
from fastapi import Depends


router = APIRouter(
    prefix="/order",
    tags=["Pedidos"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order_for_user(order: OrderCreate, db: db_dependency, current_user: User = Depends(verify_roles(["user"]))):
    return create_user_order(db=db, order=order, user_id=current_user.id)


@router.get("/", response_model=List[Order])
async def get_orders_for_seller(db: db_dependency, current_user: User = Depends(verify_roles(["seller"]))):
    return get_orders(db)
