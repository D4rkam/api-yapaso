# from typing import Optional

# from sqlalchemy.orm import Session

# from app.models.user_model import Seller


# class SellerRepository:
#     def __init__(self, db_session: Session):
#         self.db_session = db_session


# def get_linked_mp_seller_by_email(self, email: str) -> Optional[Seller]:
#     # Esta funcion debe retornar true o false dependiendo si el campo mp_access_token esta completo o no.
#     mp_linked_seller = (
#         self.db_session.query(Seller)
#         .filter(Seller.email == email, Seller.mp_access_token.isnot(None))
#         .first()
#     )
#     return mp_linked_seller is not None
