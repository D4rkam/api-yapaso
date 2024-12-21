from fastapi import FastAPI, Request, status
from starlette.responses import JSONResponse
import signal
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from app.controllers.auth_controller import router as router_auth
from app.controllers.user_controller import router as router_user
from app.controllers.order_controller import router as router_order
from app.controllers.product_controller import router as router_product
from app.controllers.pay_controller import router as router_pay
from app.controllers.ws_controller import router as router_ws
from app.database import engine, Base
from app.logger import access_logger
import requests as rq


app = FastAPI(debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todas las cabeceras
)
# app.add_middleware(HTTPSRedirectMiddleware)

app.include_router(prefix="/api", router=router_auth)
app.include_router(prefix="/api", router=router_user)
app.include_router(prefix="/api", router=router_order)
app.include_router(prefix="/api", router=router_product)
app.include_router(prefix="/api", router=router_pay)
app.include_router(prefix="/api", router=router_ws)
# app.separate_input_output_schemas = True

# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app.title = "Ya Paso API"


@app.middleware("http")
async def restrict_ips(request: Request, call_next):
    client_ip = request.client.host
    if client_ip == "127.0.0.1" or "181.166.149.116":
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


# def handle_exit(signal, frame):
#     import colorama
#     print("==================================")
#     print(f"{colorama.Fore.RED}{
#           colorama.Style.BRIGHT}[-] Saliendo...{colorama.Fore.RESET}{colorama.Style.RESET_ALL}")
#     print("==================================")
#     import sys
#     sys.exit(0)


# signal.signal(signal.SIGINT, handle_exit)
# signal.signal(signal.SIGTERM, handle_exit)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(host="0.0.0.0", port=8000, app=app)
