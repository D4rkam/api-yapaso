from typing import Generator

from sqlalchemy import URL, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from app.config import get_settings

Base = declarative_base()


def get_engine():
    settings = get_settings()
    SQLALCHEMY_DATABASE_URL = URL.create(
        drivername="mysql",
        username=settings.DB_USER,
        password=settings.DB_PASSWORD.get_secret_value(),
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_DATABASE,
    )
    return create_engine(SQLALCHEMY_DATABASE_URL)


def get_session_local():
    engine = get_engine()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return Session()


def get_db() -> Generator[Session, None, None]:
    """
    Dependencia para obtener una sesión de base de datos.
    Abre una conexión a la base de datos y la cierra después de usarla.
    """
    db = get_session_local()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=get_engine())


def drop_db():
    Base.metadata.drop_all(bind=get_engine())
    Base.metadata.drop_all(bind=get_engine())
