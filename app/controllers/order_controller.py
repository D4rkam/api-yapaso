from typing import List

from fastapi import APIRouter, status

from app.dependencies.db import db_dependency
from app.dependencies.security import seller_dependency, user_dependency
from app.schemas.order_schema import Order, OrderCreate
from app.services.order_service import OrderService


class OrderController:
    def __init__(self):
        self.router = APIRouter(prefix="/order", tags=["Pedidos"])
        self.router.add_api_route(
            "/",
            self.create_order_for_user,
            methods=["POST"],
            status_code=status.HTTP_200_OK,
            response_model=Order,
        )
        self.router.add_api_route(
            "/", self.get_orders_for_seller, methods=["GET"], response_model=List[Order]
        )

    @staticmethod
    async def create_order_for_user(
        order: OrderCreate,
        db: db_dependency,
        current_user: user_dependency,
    ):
        return await OrderService(db_session=db).create_user_order(order=order)

    @staticmethod
    async def get_orders_for_seller(
        db: db_dependency, current_seller: seller_dependency
    ):
        return await OrderService(db_session=db).get_orders(
            seller_id=current_seller.id,
        )
