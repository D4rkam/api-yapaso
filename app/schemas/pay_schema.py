from pydantic import BaseModel
from typing import List


class Item(BaseModel):
    title: str
    quantity: int = 1
    unit_price: int


class PreferenceProductsRequest(BaseModel):
    items: List[Item]
    back_urls: dict[str, str] = {
        "success": "https://www.yapaso.com/success",
        "pending": "https://www.yapaso.com/pending",
        "failure": "https://www.yapaso.com/failure"
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
