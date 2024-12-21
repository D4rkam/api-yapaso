from app.schemas.order_schema import Order as OrderSchema


def serialize_order(order: OrderSchema):
    return {
        "id": order.id,
        "user_id": order.user_id,
        "seller_id": order.seller_id,
        "datetime_order": order.datetime_order,
        "created_at": order.created_at,
        "status": order.status,
        "total": order.total,
        "products": [
            {
                "id": product.id,
                "title": product.title,
                "price": product.price,
                "quantity": product.quantity,

            } for product in order.products
        ]
    }
