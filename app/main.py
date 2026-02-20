from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import init_db
from app.routes import initialize_routes


def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)

settings = get_settings()
origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

initialize_routes(app)


app.title = "Ya Paso API"


@app.get("/", status_code=status.HTTP_200_OK)
async def home():
    return {"State": "Ok"}
