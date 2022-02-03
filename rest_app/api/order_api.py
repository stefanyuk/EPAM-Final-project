from apifairy import body, response, authenticate
from apifairy.decorators import other_responses
from flask import Blueprint
from rest_app import db
from rest_app.schemas import OrderSchema
from rest_app.models import Order
from rest_app.api.auth import token_auth

orders_api = Blueprint('orders_api', __name__, url_prefix='/api/v1')
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)


@orders_api.route('/orders', methods=['GET'])
@authenticate(token_auth)
@response(orders_schema)
def get_all():
    """Retrieve all orders"""
    return Order.query.all()


@orders_api.route('/orders', methods=['POST'])
@authenticate(token_auth)
@body(order_schema)
@response(order_schema, status_code=201, description='Order was created')
@other_responses({400: 'Bad request'})
def new(args):
    """Create a new order"""
    return Order.create(args)


@orders_api.route('/orders/<string:order_id>', methods=['GET'])
@authenticate(token_auth)
@response(order_schema)
@other_responses({404: 'Order not found'})
def get(order_id):
    """Retrieve an order by id"""
    return Order.query.get_or_404(order_id)


@orders_api.route('/orders/<string:order_id>', methods=['PATCH'])
@authenticate(token_auth)
@body(OrderSchema(partial=True))
@response(order_schema)
@other_responses({404: 'Order not found'})
def update(args, order_id):
    """Update an order"""
    Order.query.get_or_404(order_id)
    return Order.update(order_id, args)


@orders_api.route('/orders/<string:order_id>', methods=['DELETE'])
@authenticate(token_auth)
@other_responses({204: 'No content'})
def delete(order_id):
    """Delete order"""
    Order.delete(order_id)
    return '', 204
