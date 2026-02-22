from fastapi import APIRouter, Depends
from app.dependencies.db import db_dependency
from app.dependencies.security import seller_dependency
from app.repositories.notification_repository import get_notifications
from app.schemas.notification_schema import NotificationResponse

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("/", response_model=list[NotificationResponse])
async def list_notifications(
    current_seller: seller_dependency,
    db: db_dependency,
):
    return get_notifications(db, current_seller.id)
