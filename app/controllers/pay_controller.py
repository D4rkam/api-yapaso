from fastapi import APIRouter
from services.pay_service import create_preference_products, get_seller_access_token
from schemas.pay_schema import Item
from security import verify_roles
from models.user_model import User
from fastapi import Depends
from dependencies import db_dependency


router = APIRouter(prefix="/pay", tags=["Pagos"])


@router.post("/")
async def create_preferences(data: list[Item], seller_id: int, db: db_dependency, current_user: User = Depends(verify_roles(["user"]))):
    access_token_mp = get_seller_access_token(seller_id, db)
    return create_preference_products(data, access_token_mp)
