from rest_app import ma
from rest_app.models import OrderItem


class OrderItemSchema(ma.SQLAlchemySchema):
    class Meta:
        model = OrderItem

    id = ma.auto_field(dump_only=True)
    product_id = ma.auto_field()
    quantity = ma.auto_field(required=True)
