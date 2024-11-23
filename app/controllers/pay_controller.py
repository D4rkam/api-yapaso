from fastapi import APIRouter
from services.pay_service import create_preference_products, get_seller_access_token
from schemas.pay_schema import Item
from security import verify_roles
from models.user_model import User
from fastapi import Depends
from dependencies import db_dependency, user_dependency
from config import Settings


router = APIRouter(prefix="/pay", tags=["Pagos"])


@router.post("/")
async def create_preferences(data: list[Item], db: db_dependency, current_user: user_dependency):
    # access_token_mp = get_seller_access_token(seller_id, db)

    return create_preference_products(data, str(Settings.ACCESS_TOKEN_MP))
