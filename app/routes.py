from fastapi import FastAPI

from app.config import get_settings
from app.controllers.auth_controller import router as router_auth
from app.controllers.events_controller import router as router_events
from app.controllers.mp_oauth_controller import router as router_mp_oauth
from app.controllers.order_controller import OrderController
from app.controllers.pay_controller import router as router_pay
from app.controllers.product_controller import ProductController
from app.controllers.seller_controller import SellerController
from app.controllers.user_controller import UserController
from app.controllers.ws_controller import router as router_ws
from app.controllers.notification_controller import router as router_notifications


def initialize_routes(app: FastAPI) -> None:
    settings = get_settings()
    api_prefix = settings.API_V1_STR or "/api/v1"
    app.include_router(prefix=api_prefix, router=router_auth)
    app.include_router(prefix=api_prefix, router=UserController().router)
    app.include_router(prefix=api_prefix, router=SellerController().router)
    app.include_router(prefix=api_prefix, router=OrderController().router)
    app.include_router(prefix=api_prefix, router=router_events)
    app.include_router(prefix=api_prefix, router=ProductController().router)
    app.include_router(prefix=api_prefix, router=router_pay)
    app.include_router(prefix=api_prefix, router=router_mp_oauth)
    app.include_router(prefix=api_prefix, router=router_ws)
    app.include_router(prefix=api_prefix, router=router_notifications)
