import os
from dataclasses import dataclass
from dotenv import load_dotenv
from decouple import config

load_dotenv()


@dataclass
class Settings():
    API_V1_STR: str = config(
        "API_V1_STR", cast=str, default="/api")
    PROJECT_NAME: str = config(
        "PROJECT_NAME", cast=str, default="Ya Paso")

    DB_CONNECTION: str = config(
        "DB_CONNECTION",
        cast=str,
        default="mysql"
    )
    DB_HOST: str = config("DB_HOST", cast=str, default="localhost")
    DB_PORT: int = config("DB_PORT", default=3306, cast=int)
    DB_DATABASE: str = config("DB_DATABASE", cast=str, default="api_test")
    DB_USER: str = config("DB_USERNAME", cast=str, default="root")
    DB_PASSWORD: str = config("DB_PASSWORD", cast=str, default="")

    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ACCESS_TOKEN_MP = os.getenv("MERCADO_PAGO_TOKEN")

    class Config:
        case_sensitive = True


settings = Settings()
