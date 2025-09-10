"""
Configuración común para tests de Ya Paso API.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


# Base de datos en memoria para tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override de la dependencia de base de datos para tests."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session")
def test_db():
    """Fixture para crear/limpiar base de datos de test."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(test_db):
    """Fixture para cliente de pruebas de FastAPI."""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def db_session():
    """Fixture para sesión de base de datos de test."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_user_data():
    """Datos de ejemplo para usuario."""
    return {
        "name": "Test User",
        "last_name": "Test LastName",
        "username": "testuser",
        "password": "testpassword123",
        "file_num": 12345
    }


@pytest.fixture
def sample_product_data():
    """Datos de ejemplo para producto."""
    return {
        "name": "Test Product",
        "description": "Test Description",
        "price": 100.0,
        "stock": 10
    }


@pytest.fixture
def auth_headers(client, sample_user_data):
    """Headers de autenticación para tests."""
    # Registrar usuario
    client.post("/api/auth/register", json=sample_user_data)
    
    # Hacer login
    login_data = {
        "username": sample_user_data["username"],
        "password": sample_user_data["password"]
    }
    response = client.post("/api/auth/login", data=login_data)
    token = response.json()["access_token"]
    
    return {"Authorization": f"Bearer {token}"}