from datetime import datetime
from pydantic import BaseModel
from typing import Any

class NotificationBase(BaseModel):
    event: str
    data: dict[str, Any] | None = None
    read: bool = False
    created_at: datetime

class NotificationCreate(BaseModel):
    event: str
    data: dict[str, Any] | None = None

class NotificationResponse(NotificationBase):
    id: int
    seller_id: int

    class Config:
        orm_mode = True
