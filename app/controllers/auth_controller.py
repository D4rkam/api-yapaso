from fastapi import APIRouter, HTTPException, status
from datetime import timedelta

from schemas.user_schema import CreateUserRequest, UserLogin, ResponseUserDataToken, UserDataToken
from schemas.seller_schema import CreateSellerRequest, LoginSellerRequest
from models.user_model import User
from models.seller_model import Seller
from schemas.seller_schema import SellerDataToken
from schemas.token_schema import Token
from dependencies import db_dependency
from services.auth_service import authenticate_user, create_access_token, authenticate_seller, create_access_token_seller
from security import bcrypt_context
from services.user_service import get_user_by_username, get_user_by_file_num
from services.seller_service import get_seller_by_email

router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)


@router.post("/user", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    db_user_by_username = get_user_by_username(
        db, create_user_request.username)

    db_user_by_filenum = get_user_by_file_num(db, create_user_request.file_num)

    if db_user_by_username:
        raise HTTPException(
            status_code=400, detail="El nombre de usuario ya existe")

    if db_user_by_filenum:
        raise HTTPException(
            status_code=400, detail="El número de legajo ya existe")

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


@router.post("/user/login", response_model=ResponseUserDataToken)
async def login_for_access_token(form_user: UserLogin, db: db_dependency):
    form_user = authenticate_user(form_user.username, form_user.password, db)
    if not form_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no valido")
    token = create_access_token(
        form_user.username, form_user.id, timedelta(days=30))
    user_data = UserDataToken(
        id=form_user.id,
        name=form_user.name,
        last_name=form_user.last_name,
        username=form_user.username,
        password=form_user.hashed_password,
        file_num=str(form_user.file_num),
        orders=form_user.orders,
        balance=form_user.balance,
        token=Token(access_token=token,
                    token_type="bearer"),
        role=form_user.role
    )
    return ResponseUserDataToken(user=user_data)


@router.post("/seller", status_code=status.HTTP_201_CREATED)
async def create_seller(create_seller_request: CreateSellerRequest, db: db_dependency):
    db_seller_by_username = get_seller_by_email(
        db, create_seller_request.email)

    if db_seller_by_username:
        raise HTTPException(
            status_code=400, detail="El email ya esta registrado")

    create_seller_model = Seller(
        email=create_seller_request.email,
        name_store=create_seller_request.name_store,
        school_name=create_seller_request.school_name,
        location=create_seller_request.location,
        orders=[],
        products=[],
        hashed_password=bcrypt_context.hash(create_seller_request.password)
    )
    db.add(create_seller_model)
    db.commit()


@router.post("/seller/login", response_model=SellerDataToken)
async def login_seller(form_seller: LoginSellerRequest, db: db_dependency):
    seller_auth = authenticate_seller(
        form_seller.email, form_seller.password, db)
    if not seller_auth:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales no válidas")
    token = create_access_token_seller(
        seller_auth.email, seller_auth.id, timedelta(days=30))

    seller_data = SellerDataToken(
        id=seller_auth.id,
        email=seller_auth.email,
        password=seller_auth.hashed_password,
        name_store=seller_auth.name_store,
        school_name=seller_auth.school_name,
        location=seller_auth.location,
        orders=seller_auth.orders,
        products=seller_auth.products,
        token=Token(access_token=token,
                    token_type="bearer"),
        role=seller_auth.role
    )

    return seller_data
