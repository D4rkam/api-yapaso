from pydantic import BaseModel
from typing import List


class Item(BaseModel):
    title: str
    quantity: int = 1
    unit_price: int


class PreferenceProductsRequest(BaseModel):
    items: List[Item]
    back_urls: dict[str, str] = {
        "success": "yapaso://payment/success",
        "pending": "yapaso://payment/pending",
        "failure": "yapaso://payment/failure"
    }
    currency_id: str = "ARS"
    auto_return: str = "approved"
    payer: dict[str, str] = {
        "name": "Agustina",
        "surname": "Moreira",
        "email": "moreiraagustina886@gmail.com"
    }

    class Config:
        arbitrary_types_allowed = True
