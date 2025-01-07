from typing import Annotated

from fastapi import Depends

from app.models.seller_model import Seller
from app.models.user_model import User
from app.security import get_current_seller, get_current_user

user_dependency = Annotated[User, Depends(get_current_user)]
seller_dependency = Annotated[Seller, Depends(get_current_seller)]
