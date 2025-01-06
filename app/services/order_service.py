from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.order_model import Order
from app.models.user_model import User
from app.models.product_model import Product
from app.schemas.order_schema import OrderCreate, Order as OrderSchema
from datetime import datetime
from app.manage_websocket import manager


async def get_orders(seller_id: int, db: Session, skip: int = 0, limit: int = 100):
    """
    Esta funcion retorna todos los pedidos de la base de datos.
    Esencial para el buffet
    """
    orders = (db.query(Order)
              .filter(Order.seller_id == seller_id)
              .order_by(Order.datetime_order.desc())
              .offset(skip)
              .limit(limit)
              .all())
    serializer_orders = [OrderSchema.model_validate(
        order).model_dump() for order in orders]
    # print([OrderSchema.model_validate(order).model_dump() for order in orders])
    return serializer_orders


async def create_user_order(db: Session, order: OrderCreate) -> Order:
    """
    Esta funcion crea un pedido para un usuario.
    """
    user = db.query(User).filter(User.id == order.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    created_at = datetime.now().strftime("%Y-%m-%dT%H:%M")
    datetime_order = datetime.strptime(
        order.datetime_order, "%Y-%m-%dT%H:%M")

    db_order = Order(
        user_id=order.user_id, datetime_order=datetime_order, created_at=created_at, status="ENCARGADO")

    for product in order.products:
        db_product = db.query(Product).filter(Product.id == product.id).first()
        if db_product is None:
            raise HTTPException(status_code=404, detail=f"Producto con id: {
                product.id} no encontrado")
        db_order.products.append(db_product)

        seller_id = db_product.seller_id
        db_order.seller_id = seller_id
        db_order.total = sum([product.price for product in db_order.products])
        db.add(db_order)
        db.commit()
        db.refresh(db_order)

        return db_order
