from marshmallow import validates, ValidationError, post_dump
import datetime as dt
from rest_app import ma
from rest_app.models import Order, Product, Address, User


class OrderSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Order

    id = ma.auto_field(dump_only=True)
    status = ma.auto_field(missing='awaiting fulfilment')
    order_date = ma.auto_field(missing=dt.datetime.now().date())
    comments = ma.auto_field()
    order_time = ma.auto_field(missing=dt.datetime.now().time())
    user_id = ma.auto_field(required=True, load_only=True)
    user = ma.Pluck('UserSchema', 'username', dump_only=True)
    address_id = ma.auto_field(required=True, load_only=True)
    address = ma.Nested('AddressSchema', only=('city', 'street', 'street_number', 'postal_code'), dump_only=True)
    order_items = ma.List(ma.Nested(
        'OrderItemSchema', only=('product_id', 'quantity')), required=True
    )

    @validates('order_items')
    def validate_order_items(self, order_items):
        """Validates provided order items"""
        wrong_id_list = list()

        for info in order_items:
            if not Product.query.get(info['product_id']):
                wrong_id_list.append(info['product_id'])

        if wrong_id_list:
            raise ValidationError(
                {
                    'message': 'Some of the provided products do not exist. Please verify your data',
                    'wrong_products': wrong_id_list
                }
            )

    @validates('address_id')
    def validate_address_id(self, value):
        """Validates provided address id"""
        if not Address.query.get(value):
            raise ValidationError('Address with the provided id does not exist')

    @validates('user_id')
    def validate_user_id(self, value):
        """Validates provided user id"""
        if not User.query.get(value):
            raise ValidationError('User with the provided id does not exist')

    @post_dump
    def add_total_price(self, data, **kwargs):
        """Adds total order price to the schema dump result"""
        order = Order.query.get(data['id'])
        data['total_price'] = order.calculate_total_price()
        return data
