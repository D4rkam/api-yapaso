from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.firebase.firebase_storage import bucket
from app.models.product_model import Product
from app.repositories.product_repository import ProductRepository
from app.schemas.product_schema import ProductCreate


class ProductService:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.product_repository = ProductRepository(db_session)

    def get_product_by_id(self, product_id: int):
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    def get_products(self, skip: int = 0, limit: int = 100):
        products = self.product_repository.get_all(skip, limit)
        if not products:
            raise HTTPException(status_code=404, detail="Products not found")
        return products

    def get_products_category(self, category: str, skip: int = 0, limit: int = 100):
        products = self.product_repository.get_by_category(category, skip, limit)
        if not products:
            raise HTTPException(status_code=404, detail="Products not found")
        return products

    def create_product_db(
        self, product: ProductCreate, seller_id: int, image_file: UploadFile
    ):
        data_product = product.model_dump()
        data_product["seller_id"] = seller_id

        # Subir archivo a Firebase Storage
        blob = bucket.blob(f"products/{image_file.filename}")
        blob.upload_from_file(image_file.file, content_type=image_file.content_type)
        # Obtener la URL de descarga
        image_url = blob.public_url

        data_product["image_url"] = image_url
        db_product = Product(**data_product)
        return self.product_repository.create(db_product)

    def delete_product(self, product_id: int):
        product_delete = self.delete_product(product_id)
        if not product_delete:
            raise HTTPException(status_code=404, detail="Product not found")
