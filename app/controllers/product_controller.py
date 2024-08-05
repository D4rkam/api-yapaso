from fastapi import APIRouter, UploadFile, File, status
from dependencies import db_dependency, user_dependency
from services.product_service import get_products, delete_product, get_product_by_id, create_product_db, upload_image
from typing import List
from schemas.product_schema import Product, ProductCreate


router = APIRouter(
    prefix="/product",
    tags=["Productos"]
)


@router.get("/{product_id}", response_model=Product)
async def get_product(db: db_dependency, user: user_dependency, product_id: int):
    return get_product_by_id(db, product_id)


@router.get("/all", response_model=List[Product])
async def get_products_list(db: db_dependency, user: user_dependency):
    return get_products(db)


@router.post("/", response_model=Product)
async def create(db: db_dependency, user: user_dependency, product_model: ProductCreate, file: UploadFile = File(...)):
    return create_product_db(db, product_model)


@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
async def delete(db: db_dependency, user: user_dependency, product_id: int):
    return delete_product(db, product_id)
