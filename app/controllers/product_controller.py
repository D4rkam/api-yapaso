from typing import List

from fastapi import APIRouter, File, Form, UploadFile, status

from app.controllers.events_controller import SSEEvent
from app.dependencies.db import db_dependency
from app.dependencies.security import seller_dependency, user_dependency
from app.schemas.event_schema import EventSchema
from app.schemas.product_schema import Product, ProductCreate
from app.services.product_service import (
    create_product_db,
    delete_product,
    get_product_by_id,
    get_products,
    get_products_category,
)

router = APIRouter(prefix="/product", tags=["Productos"])


@router.get("/{product_id}", response_model=Product)
async def get_product(
    db: db_dependency, product_id: int, current_user: seller_dependency
):
    return get_product_by_id(db, product_id)


@router.get("/", response_model=List[Product])
async def get_products_list(db: db_dependency, current_user: user_dependency):
    return get_products(db)


@router.get("/category/{category}", response_model=List[Product])
async def get_products_for_category(
    db: db_dependency, current_user: user_dependency, category: str
):
    return get_products_category(db, category=category)


@router.post("/", response_model=Product)
async def create(
    db: db_dependency,
    current_user: seller_dependency,
    name_product: str = Form(...),
    desc_product: str = Form(...),
    price_product: int = Form(...),
    quantity_product: int = Form(...),
    category: str = Form(...),
    file: UploadFile = File(...),
):
    product_model = ProductCreate(
        name=name_product,
        description=desc_product,
        price=price_product,
        quantity=quantity_product,
        category=category,
    )
    SSEEvent.add_event(
        EventSchema(type="new_product", message=product_model.model_dump_json())
    )
    return create_product_db(db, product_model, current_user.id, file)


@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
async def delete(db: db_dependency, product_id: int, current_user: seller_dependency):
    return delete_product(db, product_id)
