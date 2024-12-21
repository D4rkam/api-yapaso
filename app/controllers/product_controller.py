from fastapi import APIRouter, UploadFile, File, status, Form, Query
from app.dependencies import db_dependency, user_dependency, seller_dependency
from app.services.product_service import get_products, delete_product, get_product_by_id, create_product_db, get_products_category
from typing import List
from app.schemas.product_schema import Product, ProductCreate


router = APIRouter(
    prefix="/product",
    tags=["Productos"]
)


@router.get("/{product_id}", response_model=Product)
async def get_product(db: db_dependency, product_id: int, current_user: seller_dependency):
    return get_product_by_id(db, product_id)


@router.get("/", response_model=List[Product])
async def get_products_list(db: db_dependency, current_user: user_dependency):
    return get_products(db)


@router.get("/category/{category}", response_model=List[Product])
async def get_products_for_category(db: db_dependency, current_user: user_dependency, category: str):
    return get_products_category(db, category=category)


@router.post("/", response_model=Product)
async def create(db: db_dependency,
                 current_user: seller_dependency,
                 name_product: str = Form(...),
                 desc_product: str = Form(...),
                 price_product: int = Form(...),
                 quantity_product: int = Form(...),
                 category: str = Form(...),
                 file: UploadFile = File(...)):

    product_model = ProductCreate(
        name=name_product, description=desc_product, price=price_product, quantity=quantity_product, category=category)
    return create_product_db(db, product_model, current_user.id, file)


@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
async def delete(db: db_dependency, product_id: int, current_user: seller_dependency):
    return delete_product(db, product_id)
