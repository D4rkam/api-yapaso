# Guía de Desarrollo - Ya Paso API

## Configuración del Entorno de Desarrollo

### 1. Instalación Inicial

```bash
# Clonar el repositorio
git clone https://github.com/D4rkam/api-yapaso.git
cd api-yapaso

# Configurar entorno de desarrollo
make setup-dev
```

### 2. Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp app/.env.example app/.env

# Editar configuraciones
nano app/.env
```

### 3. Usando Docker (Recomendado)

```bash
# Levantar todos los servicios
make docker-up-dev

# Ver logs
make docker-logs

# Acceder a la API
curl http://localhost:8000/health
```

### 4. Desarrollo Local (Sin Docker)

```bash
# Instalar dependencias
make install-dev

# Ejecutar servidor de desarrollo
make dev

# En otra terminal, ejecutar tests
make test
```

## Comandos Útiles

### Desarrollo
```bash
make dev          # Servidor de desarrollo
make test         # Ejecutar tests
make lint         # Verificar código
make format       # Formatear código
make clean        # Limpiar archivos temporales
```

### Docker
```bash
make docker-up-dev    # Levantar con phpMyAdmin
make docker-down      # Detener servicios
make docker-shell     # Acceso al contenedor
make docker-db-shell  # Acceso a MySQL
```

### Base de Datos
```bash
make db-reset         # Resetear BD (desarrollo)
make backup-db        # Crear backup
```

## Estructura del Código

### Flujo de una Request

```
HTTP Request
    ↓
Controller (validación, autorización)
    ↓
Service (lógica de negocio)
    ↓
Repository (acceso a datos)
    ↓
Model (entidad de BD)
```

### Agregar Nueva Funcionalidad

1. **Crear modelo** en `app/models/`
2. **Crear esquema** en `app/schemas/`
3. **Crear repositorio** en `app/repositories/`
4. **Crear servicio** en `app/services/`
5. **Crear controlador** en `app/controllers/`
6. **Registrar ruta** en `app/routes.py`
7. **Crear tests** en `tests/`

## Testing

### Ejecutar Tests
```bash
# Todos los tests
pytest

# Por categoría
pytest -m unit
pytest -m integration
pytest -m e2e

# Con cobertura
pytest --cov=app
```

### Escribir Tests
```python
# Test unitario
@pytest.mark.unit
def test_service_method():
    # Arrange
    service = UserService()
    
    # Act
    result = service.method()
    
    # Assert
    assert result is not None

# Test de integración
@pytest.mark.integration
def test_api_endpoint(client):
    response = client.get("/api/users/")
    assert response.status_code == 200
```

## Estilo de Código

### Formateo
- **Black** para formateo automático
- **Flake8** para linting
- **MyPy** para verificación de tipos

### Convenciones
- Nombres de archivos: `snake_case`
- Clases: `PascalCase`
- Funciones/variables: `snake_case`
- Constantes: `UPPER_CASE`

### Documentación
```python
def function_name(param: str) -> dict:
    """
    Descripción breve de la función.
    
    Args:
        param: Descripción del parámetro
        
    Returns:
        Descripción del valor de retorno
        
    Raises:
        ExceptionType: Descripción de cuándo se lanza
    """
    pass
```

## Git Workflow

### Branches
- `main`: Código de producción
- `develop`: Código de desarrollo
- `feature/nombre`: Nuevas funcionalidades
- `bugfix/nombre`: Corrección de bugs
- `hotfix/nombre`: Fixes críticos para producción

### Commits
```bash
# Formato de commit
tipo(scope): descripción breve

# Tipos: feat, fix, docs, style, refactor, test, chore
# Ejemplos:
feat(auth): add JWT token validation
fix(database): resolve connection pool issue
docs(readme): update installation instructions
```

### Pull Requests
1. Crear branch desde `develop`
2. Implementar cambios
3. Ejecutar tests y linting
4. Hacer commit y push
5. Crear PR hacia `develop`
6. Code review
7. Merge cuando esté aprobado

## Debugging

### Logs
```python
from app.logger import logger

logger.info("Información general")
logger.warning("Advertencia")
logger.error("Error", exc_info=True)
```

### Debug en Development
```bash
# Ejecutar con debug
make dev-debug

# Ver logs en tiempo real
make docker-logs
```

### Profiling
```bash
# Analizar rendimiento
pip install py-spy
py-spy record -o profile.svg -- python -m uvicorn app.main:app
```

## Despliegue

### Staging
```bash
make deploy-staging
```

### Producción
```bash
make deploy-prod
```

### Variables de Entorno en Producción
- `APP_DEBUG=false`
- `SECRET_KEY`: Clave fuerte y única
- `DB_*`: Configuraciones de BD de producción
- `MERCADO_PAGO_TOKEN`: Token de producción

## Monitoreo

### Health Checks
- `GET /`: Health check básico
- `GET /health`: Health check detallado

### Métricas
- Logs estructurados
- Tiempo de respuesta
- Errores por endpoint
- Uso de memoria/CPU

## Troubleshooting

### Problemas Comunes

**Error de conexión a BD:**
```bash
# Verificar que MySQL esté corriendo
make docker-up mysql
```

**Tests fallando:**
```bash
# Limpiar caché de pytest
make clean
pytest --cache-clear
```

**Dependencias conflictivas:**
```bash
# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

### Logs Útiles
```bash
# Logs de la API
make docker-logs api

# Logs de MySQL
make docker-logs mysql

# Logs del sistema
docker system events
```