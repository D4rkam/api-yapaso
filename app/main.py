from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.routes import initialize_routes


def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todas las cabeceras
)

initialize_routes(app)


app.title = "Ya Paso API"


@app.get("/", status_code=status.HTTP_200_OK)
async def home():
    return {"State": "Ok"}
