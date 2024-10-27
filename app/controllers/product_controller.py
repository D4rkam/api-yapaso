from fastapi import APIRouter, UploadFile, File, status, Form
from dependencies import db_dependency, user_dependency, seller_dependency
from services.product_service import get_products, delete_product, get_product_by_id, create_product_db, upload_image
from typing import List
from schemas.product_schema import Product, ProductCreate
from security import verify_roles
from models.user_model import User
from fastapi import Depends
from models.seller_model import Seller

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


@router.post("/", response_model=Product)
async def create(db: db_dependency,
                 current_user: seller_dependency,
                 name_product: str = Form(...),
                 desc_product: str = Form(...),
                 price_product: float = Form(...),
                 quantity_product: int = Form(...),
                 file: UploadFile = File(...)):

    product_model = ProductCreate(
        name=name_product, description=desc_product, price=price_product, quantity=quantity_product)
    return create_product_db(db, product_model, current_user.id, file)


@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
async def delete(db: db_dependency, product_id: int, current_user: seller_dependency):
    return delete_product(db, product_id)
