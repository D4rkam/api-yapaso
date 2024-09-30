import os
from dotenv import load_dotenv
import mercadopago
from schemas.pay_schema import PreferenceProductsRequest, Item

load_dotenv()
sdk = mercadopago.SDK(os.getenv("MERCADO_PAGO_TOKEN"))


def create_preference_products(request: list[Item]):
    preference_data = PreferenceProductsRequest(items=request)
    preference_response = sdk.preference().create(preference_data.model_dump())
    if preference_response["status"] == 201:
        return preference_response["response"]
