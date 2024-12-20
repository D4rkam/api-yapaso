from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: str
    price: int
    image_url: str = None
    quantity: int = 1
    category: str


class ProductForOrder(BaseModel):
    id: int


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    seller_id: int

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True
