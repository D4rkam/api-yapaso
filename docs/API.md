# API Documentation - Ya Paso API

## Overview

Ya Paso API es una REST API moderna construida con FastAPI que proporciona funcionalidades para gestión de usuarios, productos, órdenes y pagos.

## Base URL

```
http://localhost:8000
```

## Autenticación

La API utiliza JWT (JSON Web Tokens) para autenticación.

### Obtener Token

```http
POST /api/auth/login
Content-Type: application/x-www-form-urlencoded

username=tu_usuario&password=tu_contraseña
```

**Respuesta:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### Usar Token

Incluir el token en el header Authorization:

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

## Endpoints

### Health Check

#### GET /
Verificación básica de salud de la API.

**Respuesta:**
```json
{
  "status": "healthy",
  "service": "Ya Paso API",
  "version": "1.0.0"
}
```

#### GET /health
Verificación detallada de salud.

**Respuesta:**
```json
{
  "status": "healthy",
  "service": "Ya Paso API",
  "version": "1.0.0",
  "debug_mode": false,
  "database": "connected"
}
```

### Autenticación

#### POST /api/auth/login
Iniciar sesión de usuario.

**Parámetros:**
- `username` (string): Nombre de usuario
- `password` (string): Contraseña

**Respuesta exitosa (200):**
```json
{
  "access_token": "string",
  "token_type": "bearer",
  "expires_in": 1800
}
```

#### POST /api/auth/register
Registrar nuevo usuario.

**Body:**
```json
{
  "name": "string",
  "last_name": "string",
  "username": "string",
  "password": "string",
  "file_num": 0
}
```

### Usuarios

#### GET /api/users/
Obtener información del usuario actual.

**Headers:**
```
Authorization: Bearer <token>
```

**Respuesta (200):**
```json
{
  "User": {
    "id": 1,
    "name": "string",
    "last_name": "string",
    "username": "string",
    "file_num": 0,
    "role": "user",
    "balance": 0
  }
}
```

#### GET /api/users/{username}
Obtener usuario por nombre de usuario.

**Parámetros:**
- `username` (string): Nombre de usuario

**Respuesta (200):**
```json
{
  "id": 1,
  "name": "string",
  "last_name": "string",
  "username": "string",
  "file_num": 0,
  "role": "user",
  "balance": 0
}
```

### Productos

#### GET /api/products/
Listar todos los productos.

**Respuesta (200):**
```json
[
  {
    "id": 1,
    "name": "string",
    "description": "string",
    "price": 0,
    "stock": 0,
    "category": "string"
  }
]
```

#### POST /api/products/
Crear nuevo producto.

**Headers:**
```
Authorization: Bearer <token>
```

**Body:**
```json
{
  "name": "string",
  "description": "string",
  "price": 0,
  "stock": 0,
  "category": "string"
}
```

#### GET /api/products/{id}
Obtener producto por ID.

**Parámetros:**
- `id` (integer): ID del producto

### Órdenes

#### GET /api/orders/
Listar órdenes del usuario.

**Headers:**
```
Authorization: Bearer <token>
```

**Respuesta (200):**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "total": 0,
    "status": "pending",
    "created_at": "2024-01-01T00:00:00Z",
    "items": []
  }
]
```

#### POST /api/orders/
Crear nueva orden.

**Headers:**
```
Authorization: Bearer <token>
```

**Body:**
```json
{
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    }
  ]
}
```

#### GET /api/orders/{id}
Obtener orden por ID.

**Parámetros:**
- `id` (integer): ID de la orden

### Pagos

#### POST /api/payments/
Procesar pago.

**Headers:**
```
Authorization: Bearer <token>
```

**Body:**
```json
{
  "order_id": 1,
  "payment_method": "mercadopago",
  "amount": 100.00
}
```

## Códigos de Estado

| Código | Descripción |
|--------|-------------|
| 200 | OK - Solicitud exitosa |
| 201 | Created - Recurso creado |
| 400 | Bad Request - Datos inválidos |
| 401 | Unauthorized - No autenticado |
| 403 | Forbidden - Sin permisos |
| 404 | Not Found - Recurso no encontrado |
| 422 | Unprocessable Entity - Error de validación |
| 500 | Internal Server Error - Error del servidor |

## Errores

### Formato de Error

```json
{
  "detail": "Descripción del error",
  "error_code": "ERROR_CODE",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### Errores Comunes

#### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

#### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "username"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## Rate Limiting

- **Límite:** 100 requests por minuto por IP
- **Headers de respuesta:**
  - `X-RateLimit-Limit`: Límite total
  - `X-RateLimit-Remaining`: Requests restantes
  - `X-RateLimit-Reset`: Tiempo hasta reset

## Paginación

Para endpoints que retornan listas:

**Parámetros de query:**
- `page` (integer): Número de página (default: 1)
- `size` (integer): Elementos por página (default: 20, max: 100)

**Respuesta:**
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "size": 20,
  "pages": 5
}
```

## Filtrado y Ordenamiento

### Filtrado
```http
GET /api/products/?category=electronics&min_price=10&max_price=100
```

### Ordenamiento
```http
GET /api/products/?sort_by=price&sort_order=desc
```

## Webhooks

### MercadoPago Webhook

La API puede recibir webhooks de MercadoPago para actualizar el estado de los pagos.

```http
POST /api/webhooks/mercadopago
```

## SDK y Ejemplos

### JavaScript/Node.js

```javascript
const API_BASE = 'http://localhost:8000';

// Login
const login = async (username, password) => {
  const response = await fetch(`${API_BASE}/api/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: `username=${username}&password=${password}`
  });
  return response.json();
};

// Obtener productos
const getProducts = async (token) => {
  const response = await fetch(`${API_BASE}/api/products/`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  return response.json();
};
```

### Python

```python
import requests

API_BASE = "http://localhost:8000"

# Login
def login(username, password):
    response = requests.post(
        f"{API_BASE}/api/auth/login",
        data={"username": username, "password": password}
    )
    return response.json()

# Obtener productos
def get_products(token):
    response = requests.get(
        f"{API_BASE}/api/products/",
        headers={"Authorization": f"Bearer {token}"}
    )
    return response.json()
```

### cURL

```bash
# Login
curl -X POST "http://localhost:8000/api/auth/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=testuser&password=testpass"

# Obtener productos
curl -X GET "http://localhost:8000/api/products/" \
     -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Documentación Interactiva

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Soporte

Para reportar bugs o solicitar nuevas funcionalidades, crear un issue en el repositorio de GitHub.

---

*Documentación generada automáticamente desde el código fuente.*