from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.order_model import Order
from models.user_model import User
from models.product_model import Product
from schemas.order_schema import OrderCreate, Order as OrderSchema
from datetime import datetime
from manage_websocket import manager


def get_orders(db: Session, skip: int = 0, limit: int = 100):
    """
    Esta funcion retorna todos los pedidos de la base de datos.
    Esencial para el buffet
    """
    return db.query(Order).offset(skip).limit(limit).all()


def create_user_order(db: Session, order: OrderCreate):
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

    order_data = OrderSchema.model_validate(db_order).model_dump()
    # manager.send_new_order(seller_id, order_data)
    return db_order
