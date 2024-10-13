import os
from dotenv import load_dotenv

load_dotenv()


class Settings():
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Ya Paso"
    SQLALCHEMY_DATABASE_URI: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        case_sensitive = True


settings = Settings()
