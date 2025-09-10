from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.product_model import Product


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        return self.db.query(Product).offset(skip).limit(limit).all()

    def get_by_id(self, id: int) -> Optional[Product]:
        return self.db.query(Product).filter(Product.id == id).first()

    def get_by_category(
        self, category: str, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        return (
            self.db.query(Product)
            .filter(Product.category == category)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, product: Product) -> Product:
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def update(self, product: Product) -> Product:
        self.db.merge(product)
        self.db.commit()
        return product

    def delete(self, id: int) -> Optional[Product]:
        product = self.get_by_id(id)
        if product:
            self.db.delete(product)
            self.db.commit()
            return product
