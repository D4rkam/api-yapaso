from app.database import Base
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.ext.declarative import declared_attr
from app.firebase.firebase_storage import bucket
from app.models.order_model import order_products
from sqlalchemy import event


class Product(Base):

    """
    Product model for SQLAlchemy.
    """
    __tablename__ = "products"
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    name: Mapped[str] = Column(String(100), index=True)
    description: Mapped[str] = Column(Text, index=True)
    price: Mapped[int] = Column(Float, nullable=False)
    image_url: Mapped[str | None] = Column(String(255), nullable=True)
    quantity: Mapped[int] = Column(Integer, default=1)
    category: Mapped[str] = Column(String(50), index=True)

    orders: Mapped[list["Order"]] = relationship(  # type: ignore
        "Order", secondary=order_products, back_populates="products"
    )

    seller_id: Mapped[int] = Column(Integer, ForeignKey("sellers.id"))
    seller: Mapped["Seller"] = relationship(  # type: ignore
        "Seller", back_populates="products")

    @declared_attr
    def __mapper_args__(cls):
        return {
            'confirm_deleted_rows': False
        }

# Evento para eliminar la imagen de Firebase Storage al eliminar el producto


@event.listens_for(Product, 'before_delete')
def delete_image(mapper, connection, target):
    if target.image_url:
        try:
            blob = bucket.blob(target.image_url.replace(
                "https://storage.googleapis.com/ya-paso-api.appspot.com/images/products/", "images/products/"))
            blob.delete()
            # print(f"Deleted image {target.image_url}")
        except Exception as e:
            print(f"Failed to delete image {blob.name}: {e}")
