from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from controllers.auth_controller import router as router_auth
from controllers.user_controller import router as router_user
from controllers.order_controller import router as router_order
from controllers.product_controller import router as router_product
from controllers.pay_controller import router as router_pay
from database import engine, Base


app = FastAPI(debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todas las cabeceras
)
app.include_router(prefix="/api", router=router_auth)
app.include_router(prefix="/api", router=router_user)
app.include_router(prefix="/api", router=router_order)
app.include_router(prefix="/api", router=router_product)
app.include_router(prefix="/api", router=router_pay)
# app.separate_input_output_schemas = True

# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app.title = "Ya Paso API"


@app.get("/", status_code=status.HTTP_200_OK)
async def home():
    return {"Gretting": "Bienvenido a la API de Ya Paso"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
