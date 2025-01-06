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
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    MERCADO_PAGO_TOKEN: SecretStr = ""

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
