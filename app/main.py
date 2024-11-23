from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from controllers.auth_controller import router as router_auth
from controllers.user_controller import router as router_user
from controllers.order_controller import router as router_order
from controllers.product_controller import router as router_product
from controllers.pay_controller import router as router_pay
from database import engine, Base
from fastapi import WebSocket
from dependencies import seller_dependency


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


# html = """
# <!DOCTYPE html>
# <html>
#     <head>
#         <title>Chat</title>
#     </head>
#     <body>
#         <h1>WebSocket Chat</h1>
#         <form action="" onsubmit="sendMessage(event)">
#             <input type="text" id="messageText" autocomplete="off"/>
#             <button>Send</button>
#         </form>
#         <ul id='messages'>
#         </ul>
#         <script>
#             var ws = new WebSocket("ws://localhost:8000/ws");
#             ws.onmessage = function(event) {
#                 var messages = document.getElementById('messages')
#                 var message = document.createElement('li')
#                 var content = document.createTextNode(event.data)
#                 message.appendChild(content)
#                 messages.appendChild(message)
#             };
#             function sendMessage(event) {
#                 var input = document.getElementById("messageText")
#                 ws.send(input.value)
#                 input.value = ''
#                 event.preventDefault()
#             }
#         </script>
#     </body>
# </html>
# """


# @app.get("/socket")
# async def get():
#     return HTMLResponse(html)


# @app.websocket("/ws")
# async def get_orders_ws(ws: WebSocket):
#     await ws.accept()
#     while True:
#         data = await ws.receive_text()
#         await ws.send_text(f"La data del msj fue: {data}")


if __name__ == "__main__":
    # print("hola")
    import uvicorn
    uvicorn.run(host="0.0.0.0", port=8000, app=app)
