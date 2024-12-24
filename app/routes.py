from fastapi import FastAPI
from app.config import settings
from app.controllers.auth_controller import router as router_auth
from app.controllers.user_controller import router as router_user
from app.controllers.order_controller import router as router_order
from app.controllers.product_controller import router as router_product
from app.controllers.pay_controller import router as router_pay


def initialize_routes(app: FastAPI) -> None:
    app.include_router(prefix=settings.API_V1_STR, router=router_auth)
    app.include_router(prefix=settings.API_V1_STR, router=router_user)
    app.include_router(prefix=settings.API_V1_STR, router=router_order)
    app.include_router(prefix=settings.API_V1_STR, router=router_product)
    app.include_router(prefix=settings.API_V1_STR, router=router_pay)
