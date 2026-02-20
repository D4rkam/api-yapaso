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


# Configuración de la aplicación
settings = get_settings()
origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API moderna para gestión de usuarios, productos, órdenes y pagos",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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
        "version": "1.0.0",
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
        "database": "connected",  # TODO: Agregar verificación real de BD
    }
