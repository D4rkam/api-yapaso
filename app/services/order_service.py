from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.order_model import Order
from models.user_model import User
from models.product_model import Product
from schemas.order_schema import OrderCreate


def get_orders(db: Session, skip: int = 0, limit: int = 100):
    """
    Esta funcion retorna todos los pedidos de la base de datos.
    Esencial para el buffet
    """
    return db.query(Order).offset(skip).limit(limit).all()


def create_user_order(db: Session, order: OrderCreate, user_id: int):
    db_order = Order(user_id=user_id)
    for product in order.products:
        db_product = db.query(Product).filter(Product.id == product.id).first()
        if db_product is None:
            raise HTTPException(status_code=404, detail=f"Producto con id: {
                                product.id} no encontrado")
        db_order.products.append(db_product)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order
