# Tests para Ya Paso API

Este directorio contiene todas las pruebas del proyecto.

## Estructura

```
tests/
├── __init__.py
├── conftest.py              # Configuración común de pytest
├── unit/                    # Tests unitarios
│   ├── test_services/       # Tests de servicios
│   ├── test_repositories/   # Tests de repositorios
│   └── test_models/         # Tests de modelos
├── integration/             # Tests de integración
│   ├── test_api/           # Tests de endpoints
│   └── test_database/      # Tests de base de datos
└── e2e/                    # Tests end-to-end
    └── test_workflows/     # Tests de flujos completos
```

## Ejecución

```bash
# Todos los tests
pytest

# Solo tests unitarios
pytest tests/unit/

# Solo tests de integración
pytest tests/integration/

# Con cobertura
pytest --cov=app

# Tests específicos
pytest tests/unit/test_services/test_user_service.py
```

## Configuración

Los tests usan:
- **pytest** como framework de testing
- **pytest-asyncio** para tests asíncronos
- **httpx** para tests de API
- **pytest-cov** para cobertura
- **factory-boy** para fixtures de datos