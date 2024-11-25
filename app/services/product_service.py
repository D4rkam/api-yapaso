from models.product_model import Product
from sqlalchemy.orm import Session
from schemas.product_schema import ProductCreate
from fastapi import UploadFile, HTTPException, status
import uuid
from firebase.firebase_storage import bucket
import logging


def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()


def get_products_category(db: Session, category: str, skip: int = 0, limit: int = 100):
    return db.query(Product).filter(Product.category ==
                                    category).offset(skip).limit(limit).all()


def create_product_db(db: Session, product: ProductCreate, seller_id: int, image_file: UploadFile):
    data_product = product.model_dump()
    data_product["seller_id"] = seller_id

    # Subir archivo a Firebase Storage
    blob = bucket.blob(f"products/{image_file.filename}")
    blob.upload_from_file(
        image_file.file, content_type=image_file.content_type)
    # Obtener la URL de descarga
    image_url = blob.public_url

    data_product["image_url"] = image_url
    db_product = Product(**data_product)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def upload_image(db: Session, product_id: int, file: UploadFile):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if not product_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    try:
        # Generar un nombre de archivo único
        file_name = f"{uuid.uuid4()}.{file.filename.split('.')[-1]}"
        blob = bucket.blob(f"images/products/{file_name}")
        blob.upload_from_file(file.file)
        blob.make_public()

        # Asignar la URL pública de la imagen al producto
        product_db.image_url = blob.public_url
        db.commit()
        db.refresh(product_db)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return product_db


def delete_product(db: Session, product_id: int):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(db_product)
    db.commit()
