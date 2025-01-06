from typing import List

from fastapi import APIRouter, status

from app.dependencies.db import db_dependency
from app.dependencies.security import seller_dependency, user_dependency
from app.schemas.order_schema import Order, OrderCreate
from app.services.order_service import create_user_order, get_orders

router = APIRouter(prefix="/order", tags=["Pedidos"])


@router.post("/", status_code=status.HTTP_200_OK)
async def create_order_for_user(
    order: OrderCreate, db: db_dependency, current_user: user_dependency
):
    created_order = await create_user_order(db=db, order=order)
    return created_order


@router.get("/", response_model=List[Order])
async def get_orders_for_seller(db: db_dependency, current_seller: seller_dependency):
    return get_orders(seller_id=current_seller.id, db=db)
