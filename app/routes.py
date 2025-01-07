from fastapi import FastAPI

from app.config import get_settings
from app.controllers.auth_controller import router as router_auth
from app.controllers.events_controller import router as router_events
from app.controllers.order_controller import OrderController
from app.controllers.pay_controller import router as router_pay
from app.controllers.product_controller import router as router_product
from app.controllers.user_controller import UserController


def initialize_routes(app: FastAPI) -> None:
    settings = get_settings()
    api_prefix = settings.API_V1_STR or "/api/v1"
    app.include_router(prefix=api_prefix, router=router_auth)
    app.include_router(prefix=api_prefix, router=UserController().router)
    app.include_router(prefix=api_prefix, router=OrderController().router)
    app.include_router(prefix=api_prefix, router=router_events)
    app.include_router(prefix=api_prefix, router=router_product)
    app.include_router(prefix=api_prefix, router=router_pay)
