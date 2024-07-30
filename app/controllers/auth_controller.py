from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import Annotated

from schemas.user_schema import CreateUserRequest, UserLogin, ResponseUserDataToken
from models.user_model import User
from schemas.token_schema import Token
from dependencies import db_dependency
from services.auth_service import authenticate_user, create_access_token
from security import bcrypt_context
from services.user_service import get_user_by_username

router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    db_user = get_user_by_username(db, username=create_user_request.username)

    if db_user:
        raise HTTPException(
            status_code=400, detail="El nombre de usuario ya existe")

    create_user_model = User(
        name=create_user_request.name,
        last_name=create_user_request.last_name,
        username=create_user_request.username,
        file_num=create_user_request.file_num,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        orders=[]
    )
    db.add(create_user_model)
    db.commit()


@router.post("/login", response_model=ResponseUserDataToken)
async def login_for_access_token(form_user: UserLogin, db: db_dependency):
    form_user = authenticate_user(form_user.username, form_user.password, db)
    if not form_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no valido")
    token = create_access_token(
        form_user.username, form_user.id, timedelta(minutes=20))
    user_data = ResponseUserDataToken(
        id=form_user.id,
        name=form_user.name,
        last_name=form_user.last_name,
        username=form_user.username,
        password=form_user.hashed_password,
        file_num=str(form_user.file_num),
        orders=form_user.orders,
        token=Token(access_token=token,
                    token_type="bearer"),)
    return user_data
