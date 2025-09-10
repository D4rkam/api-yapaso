from typing import List

from sqlalchemy.orm import Session

from app.models.order_model import Order


class OrderRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_all_orders(
        self, seller_id: int, skip: int = 0, limit: int = 100
    ) -> List[Order]:
        return (
            self.db_session.query(Order)
            .filter(Order.seller_id == seller_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_all_orders_order_by_datetime(
        self,
        seller_id: int,
        skip: int = 0,
        limit: int = 100,
        desc: bool = False,
    ) -> List[Order]:
        return (
            self.db_session.query(Order)
            .filter(Order.seller_id == seller_id)
            .order_by(
                Order.datetime_order.desc() if desc else Order.datetime_order.asc()
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_order_by_id(self, order_id: int) -> Order:
        return self.db_session.query(Order).filter(Order.id == order_id).first()

    def add_order(self, order: Order) -> Order:
        self.db_session.add(order)
        self.db_session.commit()
        self.db_session.refresh(order)
        return order

    def delete_order(self, order_id: int) -> None:
        order = self.get_order_by_id(order_id)
        if order:
            self.db_session.delete(order)
            self.db_session.commit()
            self.db_session.commit()
