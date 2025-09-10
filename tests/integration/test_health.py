"""
Tests para endpoints de salud de la API.
"""
import pytest
from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    """Test del endpoint de health check básico."""
    response = client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "service" in data
    assert "version" in data


def test_detailed_health_check(client: TestClient):
    """Test del endpoint de health check detallado."""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "service" in data
    assert "version" in data
    assert "debug_mode" in data
    assert "database" in data


@pytest.mark.asyncio
async def test_health_check_content_type(client: TestClient):
    """Test que verifica el content-type de la respuesta."""
    response = client.get("/")
    
    assert response.headers["content-type"] == "application/json"