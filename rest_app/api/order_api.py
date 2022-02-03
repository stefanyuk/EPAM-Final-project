from apifairy import body, response
from apifairy.decorators import other_responses
from flask import Blueprint
from rest_app import db
from rest_app.schemas import OrderSchema
from rest_app.models import Order

orders_api = Blueprint('orders_api', __name__, url_prefix='/api/v1')
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)


@orders_api.route('/orders', methods=['GET'])
@response(orders_schema)
def get_all():
    """Retrieve all orders"""
    return Order.query.all()


@orders_api.route('/orders', methods=['POST'])
@body(order_schema)
@response(order_schema)
def new(args):
    """Create a new order"""
    return Order.create(args)


@orders_api.route('/orders/<string:order_id>', methods=['GET'])
@response(order_schema)
@other_responses({404: 'Order not found'})
def get(order_id):
    """Retrieve an order by id"""
    return Order.query.get_or_404(order_id)


@orders_api.route('/orders/<string:order_id>', methods=['PATCH'])
@body(OrderSchema(partial=True))
@response(order_schema)
@other_responses({404: 'Order not found'})
def update(args, order_id):
    """Update an order"""
    order = Order.query.get_or_404(order_id)
    order.update(args)
    db.session.commit()
    return order


@orders_api.route('/orders/<string:order_id>', methods=['DELETE'])
@other_responses({204: 'No content'})
def delete(order_id):
    """Delete order"""
    Order.query.get(order_id).delete()
    db.session.commit()
    return '', 204
