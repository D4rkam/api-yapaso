# Ya Paso API 🚀

Una API moderna construida con FastAPI para gestionar usuarios, productos, órdenes y pagos.

## 📋 Descripción

Ya Paso API es una aplicación backend robusta que implementa una arquitectura limpia con separación de responsabilidades. Utiliza FastAPI como framework web, SQLAlchemy como ORM, y sigue las mejores prácticas de desarrollo.

## 🏗️ Arquitectura

El proyecto sigue una arquitectura en capas:

```
app/
├── controllers/     # Controladores (endpoints de la API)
├── services/        # Lógica de negocio
├── repositories/    # Capa de acceso a datos
├── models/          # Modelos de SQLAlchemy (entidades de BD)
├── schemas/         # Esquemas de Pydantic (validación/serialización)
├── dependencies/    # Dependencias de FastAPI
├── firebase/        # Integración con Firebase
├── config.py        # Configuración de la aplicación
├── database.py      # Configuración de base de datos
├── main.py          # Punto de entrada de la aplicación
└── routes.py        # Configuración de rutas
```

## 🛠️ Tecnologías

- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM para Python
- **Pydantic** - Validación de datos y serialización
- **MySQL** - Base de datos relacional
- **Firebase** - Servicios de backend
- **MercadoPago** - Integración de pagos
- **JWT** - Autenticación basada en tokens

## 📦 Instalación

### Prerrequisitos

- Python 3.8+
- MySQL 5.7+
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/D4rkam/api-yapaso.git
   cd api-yapaso
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   ```bash
   cp app/.env.example app/.env
   # Editar app/.env con tus configuraciones
   ```

5. **Configurar base de datos**
   - Crear una base de datos MySQL
   - Actualizar las variables de conexión en `app/.env`

## ⚙️ Configuración

Crear el archivo `app/.env` con las siguientes variables:

```env
# Base de datos
DB_HOST=localhost
DB_PORT=3306
DB_DATABASE=yapaso_db
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña

# Seguridad
SECRET_KEY=tu_clave_secreta_muy_segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# MercadoPago
MERCADO_PAGO_TOKEN=tu_token_de_mercadopago

# Aplicación
APP_DEBUG=False
PROJECT_NAME=Ya Paso API
API_V1_STR=/api
```

## 🚀 Uso

### Ejecutar la aplicación

```bash
# Desarrollo
uvicorn app.main:app --reload

# Producción
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Acceder a la documentación

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📚 Endpoints principales

### Autenticación
- `POST /api/auth/login` - Iniciar sesión
- `POST /api/auth/register` - Registrar usuario

### Usuarios
- `GET /api/users/` - Obtener usuario actual
- `GET /api/users/{username}` - Obtener usuario por nombre

### Productos
- `GET /api/products/` - Listar productos
- `POST /api/products/` - Crear producto
- `GET /api/products/{id}` - Obtener producto por ID

### Órdenes
- `GET /api/orders/` - Listar órdenes
- `POST /api/orders/` - Crear orden
- `GET /api/orders/{id}` - Obtener orden por ID

### Pagos
- `POST /api/payments/` - Procesar pago

## 🧪 Testing

```bash
# Ejecutar tests (cuando estén implementados)
pytest

# Con cobertura
pytest --cov=app
```

## 🐳 Docker

```bash
# Construir imagen
docker build -t yapaso-api .

# Ejecutar contenedor
docker run -p 8000:8000 yapaso-api
```

## 📁 Estructura de directorios detallada

```
ya-paso-api/
│
├── app/
│   ├── __init__.py
│   ├── main.py                    # Punto de entrada FastAPI
│   ├── config.py                  # Configuración con Pydantic
│   ├── database.py                # Configuración SQLAlchemy
│   ├── routes.py                  # Registro de rutas
│   ├── logger.py                  # Configuración de logging
│   ├── security.py                # Utilidades de seguridad
│   ├── serializers.py             # Serializadores personalizados
│   ├── manage_websocket.py        # Gestión de WebSockets
│   │
│   ├── controllers/               # Controladores (Capa de presentación)
│   │   ├── __init__.py
│   │   ├── auth_controller.py     # Autenticación y autorización
│   │   ├── user_controller.py     # Gestión de usuarios
│   │   ├── product_controller.py  # Gestión de productos
│   │   ├── order_controller.py    # Gestión de órdenes
│   │   ├── seller_controller.py   # Gestión de vendedores
│   │   ├── events_controller.py   # Gestión de eventos
│   │   └── pay_controller.py      # Gestión de pagos
│   │
│   ├── services/                  # Servicios (Lógica de negocio)
│   │   ├── __init__.py
│   │   ├── auth_service.py        # Lógica de autenticación
│   │   ├── user_service.py        # Lógica de usuarios
│   │   ├── product_service.py     # Lógica de productos
│   │   ├── order_service.py       # Lógica de órdenes
│   │   ├── seller_service.py      # Lógica de vendedores
│   │   ├── event_service.py       # Lógica de eventos
│   │   └── pay_service.py         # Lógica de pagos
│   │
│   ├── repositories/              # Repositorios (Acceso a datos)
│   │   ├── __init__.py
│   │   ├── user_repository.py     # Acceso a datos de usuarios
│   │   ├── product_repository.py  # Acceso a datos de productos
│   │   └── order_repository.py    # Acceso a datos de órdenes
│   │
│   ├── models/                    # Modelos SQLAlchemy
│   │   ├── __init__.py
│   │   ├── user_model.py          # Modelo de usuario
│   │   ├── product_model.py       # Modelo de producto
│   │   ├── order_model.py         # Modelo de orden
│   │   ├── seller_model.py        # Modelo de vendedor
│   │   └── stock_model.py         # Modelo de stock
│   │
│   ├── schemas/                   # Esquemas Pydantic
│   │   ├── __init__.py
│   │   ├── user_schema.py         # Esquemas de usuario
│   │   ├── product_schema.py      # Esquemas de producto
│   │   ├── order_schema.py        # Esquemas de orden
│   │   ├── seller_schema.py       # Esquemas de vendedor
│   │   ├── event_schema.py        # Esquemas de eventos
│   │   ├── token_schema.py        # Esquemas de tokens
│   │   └── pay_schema.py          # Esquemas de pagos
│   │
│   ├── dependencies/              # Dependencias FastAPI
│   │   ├── __init__.py
│   │   ├── db.py                  # Dependencia de base de datos
│   │   ├── security.py            # Dependencias de seguridad
│   │   └── settings.py            # Dependencias de configuración
│   │
│   └── firebase/                  # Integración Firebase
│       ├── __init__.py
│       └── ...
│
├── requirements.txt               # Dependencias Python
├── .gitignore                    # Archivos ignorados por Git
├── .env.example                  # Plantilla de variables de entorno
├── Dockerfile                    # Configuración Docker
├── docker-compose.yml            # Orquestación Docker
└── README.md                     # Documentación del proyecto
```

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👥 Autores

- **D4rkam** - *Desarrollador inicial* - [D4rkam](https://github.com/D4rkam)

## 🆘 Soporte

Si tienes algún problema o pregunta, por favor:

1. Revisa la documentación
2. Busca en los issues existentes
3. Crea un nuevo issue si es necesario

## 📈 Roadmap

- [ ] Implementar tests unitarios y de integración
- [ ] Agregar documentación de API con ejemplos
- [ ] Implementar sistema de caché con Redis
- [ ] Agregar rate limiting
- [ ] Implementar sistema de notificaciones
- [ ] Agregar métricas y monitoreo
- [ ] Implementar CI/CD pipeline
- [ ] Dockerizar completamente la aplicación