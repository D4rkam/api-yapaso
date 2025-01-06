from fastapi import APIRouter, HTTPException, status
from app.dependencies.db import db_dependency
from app.dependencies.security import user_dependency
from app.schemas.user_schema import User as UserSchema
from app.services.user_service import get_users, add_balance, substract_balance, get_user_by_username
from app.models.user_model import User


router = APIRouter(
    prefix="/users",
    tags=["Usuarios"]
)


@router.get("/", status_code=status.HTTP_200_OK)
async def user(current_user: user_dependency):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Fallo la autenticación")

    return {"User": current_user}


# @router.get("/all", response_model=List[UserSchema])
# async def users(db: db_dependency, current_user: User = Depends(verify_roles(["admin"]))):
#     return get_users(db)


@router.get("/{username}")
async def user_for_username(db: db_dependency, username: str, current_user: user_dependency):
    return get_user_by_username(db, username)


# @router.put("/balance/add")
# async def update_add_balance(db: db_dependency, current_user: user_dependency):
#     return add_balance(db, current_user.id)


# @router.put("/balance/substract")
# async def update_substract_balance(db: db_dependency, current_user: user_dependency):
#     return substract_balance(db, current_user.id)
