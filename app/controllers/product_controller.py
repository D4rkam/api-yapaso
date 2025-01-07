from typing import List

from fastapi import APIRouter, File, Form, UploadFile, status

from app.controllers.events_controller import SSEEvent
from app.dependencies.db import db_dependency
from app.dependencies.security import seller_dependency, user_dependency
from app.schemas.event_schema import EventSchema
from app.schemas.product_schema import Product, ProductCreate
from app.services.product_service import ProductService


class ProductController:
    def __init__(self):
        self.router = APIRouter(prefix="/product", tags=["Productos"])
        self.router.add_api_route(
            "/{product_id}",
            self.get_product,
            methods=["GET"],
            response_model=Product,
        )
        self.router.add_api_route(
            "/",
            self.get_products_list,
            methods=["GET"],
            response_model=List[Product],
        )
        self.router.add_api_route(
            "/category/{category}",
            self.get_products_for_category,
            methods=["GET"],
            response_model=List[Product],
        )
        self.router.add_api_route(
            "/",
            self.create_product,
            methods=["POST"],
            response_model=Product,
        )
        self.router.add_api_route(
            "/{product_id}",
            self.delete_product,
            methods=["DELETE"],
            status_code=status.HTTP_200_OK,
        )

    @staticmethod
    async def get_product(
        db: db_dependency, product_id: int, current_user: seller_dependency
    ):
        service = ProductService(db_session=db)
        return service.get_product_by_id(product_id)

    @staticmethod
    async def get_products_list(db: db_dependency, current_user: user_dependency):
        service = ProductService(db_session=db)
        return service.get_products()

    @staticmethod
    async def get_products_for_category(
        db: db_dependency, current_user: user_dependency, category: str
    ):
        service = ProductService(db_session=db)
        return service.get_products_category(category=category)

    @staticmethod
    async def create_product(
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
        service = ProductService(db_session=db)
        return service.create_product_db(product_model, current_user.id, file)

    @staticmethod
    async def delete_product(
        db: db_dependency, product_id: int, current_user: seller_dependency
    ):
        service = ProductService(db_session=db)
        return service.delete_product(product_id)
