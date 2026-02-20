from fastapi import APIRouter, HTTPException, status

from app.dependencies.security import seller_dependency


class SellerController:
    def __init__(self):
        self.router = APIRouter(prefix="/sellers", tags=["Vendedores"])
        self.router.add_api_route(
            "/",
            self.get_current_seller,
            methods=["GET"],
            status_code=status.HTTP_200_OK,
        )

    @staticmethod
    async def get_current_seller(
        current_seller: seller_dependency,
    ):
        if current_seller is None:
            raise HTTPException(status_code=401, detail="Fallo la autenticación")
        return {"Seller": current_seller}
