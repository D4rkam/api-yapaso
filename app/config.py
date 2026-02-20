from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="app/.env", env_file_encoding="utf-8")
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Ya Paso"
    APP_DEBUG: bool = False

    DB_CONNECTION: str = "mysql"
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_DATABASE: str = "api_test"
    DB_USER: str = "root"
    DB_PASSWORD: SecretStr = ""

    SECRET_KEY: SecretStr = "supersecretkey"
    REFRESH_SECRET_KEY: SecretStr = "supersecretrefreshkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7  # 7 días en minutos

    # CORS y cookies
    CORS_ORIGINS: str = ""  # Separados por coma
    COOKIE_SECURE: bool = False  # True cuando usás túnel/HTTPS
    COOKIE_SAMESITE: str = "lax"  # "none" cuando usás túnel (dominios distintos)

    MERCADO_PAGO_TOKEN: SecretStr = ""

    # OAuth Mercado Pago
    MP_CLIENT_ID: str = ""
    MP_CLIENT_SECRET: SecretStr = ""
    MP_REDIRECT_URI: str = ""  # Cambiar por la URL real de tu frontend
    FERNET_KEY: SecretStr = ""  # Generar con: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

    # class Config:
    #     env_file = "app/.env"  # Asegura que cargue el archivo .env
    #     env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """
    Carga las configuraciones usando Pydantic.
    Utiliza lru_cache para evitar recrear instancias innecesarias.
    """
    return Settings()
