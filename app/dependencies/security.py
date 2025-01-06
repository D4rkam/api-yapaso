from fastapi import Depends
from typing import Annotated
from app.security import get_current_seller, get_current_user

user_dependency = Annotated[dict, Depends(get_current_user)]
seller_dependency = Annotated[dict, Depends(get_current_seller)]
