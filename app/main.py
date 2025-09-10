from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import init_db
from app.routes import initialize_routes


def lifespan(app: FastAPI):
    """
    Lifespan events para inicializar y limpiar recursos.
    """
    init_db()
    yield


def get_cors_origins():
    """
    Obtiene los orígenes permitidos para CORS desde configuración.
    En desarrollo permite localhost, en producción usa configuración específica.
    """
    settings = get_settings()
    if settings.APP_DEBUG:
        return [
            "http://localhost:3000",
            "http://localhost:3001", 
            "http://localhost:8080",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:3001",
            "http://127.0.0.1:8080"
        ]
    # En producción, usa orígenes específicos desde configuración
    return ["*"]  # TODO: Configurar orígenes específicos en producción


# Configuración de la aplicación
settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API moderna para gestión de usuarios, productos, órdenes y pagos",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Inicializar rutas
initialize_routes(app)


@app.get("/", status_code=status.HTTP_200_OK, tags=["Health"])
async def health_check():
    """
    Endpoint de verificación de salud de la API.
    """
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": "1.0.0"
    }


@app.get("/health", status_code=status.HTTP_200_OK, tags=["Health"])
async def detailed_health_check():
    """
    Endpoint detallado de verificación de salud.
    """
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": "1.0.0",
        "debug_mode": settings.APP_DEBUG,
        "database": "connected"  # TODO: Agregar verificación real de BD
    }
