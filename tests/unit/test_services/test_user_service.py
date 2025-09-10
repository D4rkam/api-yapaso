"""
Tests unitarios para el servicio de usuarios.
"""
import pytest
from unittest.mock import Mock, patch

from app.services.user_service import UserService


class TestUserService:
    """Tests para UserService."""
    
    def setup_method(self):
        """Configuración para cada test."""
        self.user_service = UserService()
    
    @patch('app.services.user_service.UserRepository')
    def test_user_service_initialization(self, mock_repo):
        """Test de inicialización del servicio."""
        service = UserService()
        assert service is not None
    
    def test_user_service_exists(self):
        """Test que verifica que el servicio existe."""
        assert hasattr(self.user_service, '__class__')
        assert self.user_service.__class__.__name__ == 'UserService'