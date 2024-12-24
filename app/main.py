from fastapi import FastAPI, Request, status
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.logger import access_logger
from app.routes import initialize_routes
import requests as rq


app = FastAPI(debug=True)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todas las cabeceras
)

initialize_routes(app)

# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app.title = "Ya Paso API"


@app.middleware("http")
async def restrict_ips(request: Request, call_next):
    client_ip = request.client.host
    if client_ip in ["127.0.0.1", "181.166.149.116"]:
        return await call_next(request)

    resp = rq.get(
        url=f"https://api.ip2location.io/?key=AE7E86FD037692F0DC975B6FE8C7AEF8&ip={client_ip}")
    if resp.json()["country_name"] == "Buenos Aires":
        access_logger.info(f"Access granted for IP: {client_ip}")
        return await call_next(request)

    access_logger.warning(f"Access denied for IP: {client_ip}")
    raise JSONResponse(status_code=403, content={
        "detail": "Access Denied. Your IP is not authorized to access this resource."})


@app.get("/", status_code=status.HTTP_200_OK)
async def home():
    return {"State": "Ok"}
