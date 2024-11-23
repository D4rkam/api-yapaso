import mercadopago
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.seller_model import Seller
from schemas.pay_schema import PreferenceProductsRequest, Item


def create_preference_products(request: list[Item], access_token: str):
    sdk = mercadopago.SDK(access_token)
    preference_data = PreferenceProductsRequest(items=request)
    preference_response = sdk.preference().create(preference_data.model_dump())
    if preference_response["status"] == 400:
        raise HTTPException(
            status_code=400, detail=preference_response["response"])
    if preference_response["status"] == 201:
        return preference_response["response"]


def verify_seller(seller_id: int, db: Session):
    seller = db.query(Seller).filter(Seller.id == seller_id).first()
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    return seller


def get_seller_access_token(seller_id: int, db: Session):
    seller = verify_seller(seller_id, db)
    if seller.access_token is None:
        raise HTTPException(
            status_code=400, detail="Seller does not have access token")
    return seller.access_token
