from fastapi import APIRouter
from services.pay_service import create_preference_products
from schemas.pay_schema import Item
from security import verify_roles
from models.user_model import User
from fastapi import Depends


router = APIRouter(prefix="/pay", tags=["Pagos"])


@router.post("/")
async def create_preferences(data: list[Item], current_user: User = Depends(verify_roles(["user"]))):
    return create_preference_products(data)


@router.post("/pay/token")
async def pay_token(current_user: User = Depends(verify_roles(["user"]))):
    return
