from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.order_model import Order
from app.repositorys.order_repository import OrderRepository
from app.repositorys.product_repository import ProductRepository
from app.repositorys.user_repository import UserRepository
from app.schemas.order_schema import Order as OrderSchema
from app.schemas.order_schema import OrderCreate


class OrderService:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.order_repository = OrderRepository(db_session)
        self.product_repository = ProductRepository(db_session)
        self.user_repository = UserRepository(db_session)

    async def get_orders(self, seller_id: int, skip: int = 0, limit: int = 100):
        """
        Esta funcion retorna todos los pedidos de la base de datos.
        Esencial para el buffet
        """
        orders = self.order_repository.get_all_orders_order_by_datetime(
            seller_id=seller_id, skip=skip, limit=limit, desc=True
        )
        serializer_orders: list[OrderSchema] = [
            OrderSchema.model_validate(order).model_dump() for order in orders
        ]
        # print([OrderSchema.model_validate(order).model_dump() for order in orders])
        return serializer_orders

    async def create_user_order(self, order: OrderCreate) -> Order:
        """
        Esta funcion crea un pedido para un usuario.
        """
        user = self.user_repository.get_user_by_id(order.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        created_at = datetime.now().strftime("%Y-%m-%dT%H:%M")
        datetime_order = datetime.strptime(order.datetime_order, "%Y-%m-%dT%H:%M")

        db_order = Order(
            user_id=order.user_id,
            datetime_order=datetime_order,
            created_at=created_at,
            status="ENCARGADO",
        )

        for product in order.products:
            db_product = self.product_repository.get_by_id(product.id)
            if db_product is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Producto con id: {
                    product.id} no encontrado",
                )
            db_order.products.append(db_product)

            seller_id = db_product.seller_id
            db_order.seller_id = seller_id
            db_order.total = sum([product.price for product in db_order.products])

            self.order_repository.add_order(db_order)

            return db_order
