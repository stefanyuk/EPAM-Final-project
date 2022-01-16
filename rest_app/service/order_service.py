from flask_restful import reqparse
from uuid import uuid4
from datetime import datetime
from rest_app import db
from rest_app.service.order_item_service import create_order_items, update_order_items
from rest_app.service.common_services import get_row_by_id
from rest_app.models import Order, Product, User


def get_order_products_total_price(products: list):
    """
    Returns a total price of ordered products

    :param products: products ordered by a client
    """
    total_price = 0

    for product in products:
        product = Product.query.get(product['id'])
        total_price += product.price * product['quantity']

    return total_price


def create_order(products: list, user_id, address_id=None, comments=None, status=None):
    """
    Creates new order in the database

    :param products: products ordered by a client
    :param comments: comments that customer left for this order
    :param user_id: unique id of a customer
    :param status: status of the order
    :param address_id: address where order needs to be delivered
    """
    user = User.query.get(user_id)

    order = Order(
        id=str(uuid4()),
        status=status if status else 'awaiting fulfilment',
        order_date=datetime.now().date(),
        comments=comments,
        user_id=user_id,
        order_time=datetime.now().time(),
        total_price=get_order_products_total_price(products),
        address_id=address_id if address_id else user.addresses.first().id
    )

    db.session.add(order)
    db.session.commit()

    create_order_items(products, order.id, main_key='id')

    return order


def order_data_to_dict(order):
    order_data = {
        'id': order.id,
        'status': order.status,
        'order_date': str(order.order_date),
        'order_time': str(order.order_time)[:8],
        'customer_id': order.user_id,
        'total_price': float(order.total_price),
        'order_items': [order_item.product.title for order_item in order.order_items]
    }

    return order_data


def verify_product_names(products):
    """
    Verifies whether user provided correct product names

    :param products: list of product names
    """
    products_not_found = []

    for title in products:
        product = db.session.query(Product).filter(Product.title == title).first()
        if not product:
            products_not_found.append(title)

    return products_not_found


def get_all_client_orders(user_id):
    """
    Returns a list of all client's orders from the database and information about them

    :param user_id: unique customer id
    """
    query = Order.query.filter_by(user_id=user_id)

    return query


def update_order(order_id, **kwargs):
    """
    Update information about existing order

    :param order_id: unique id of the order
    """

    order = get_row_by_id(Order, order_id)
    items_except_products = {k: kwargs[k] for k in list(kwargs)[:-1]}

    if products := kwargs['products']:
        update_order_items(products, order.id)

    for key, value in items_except_products.items():
        if value:
            setattr(order, key, value)


def create_order_data_parser():
    parser = reqparse.RequestParser()

    parser.add_argument('comments', type=str)
    parser.add_argument('user_id', type=str, help='you did not provide user id', required=True)
    parser.add_argument('products', type=str, action='append', help='you did not provide products', required=True)

    return parser


def update_order_data_parser():
    parser = create_order_data_parser().copy()
    parser.add_argument('status', type=str, help='status of the order')

    return parser


def get_orders_by_status(status):
    """
    Creates a query to obtain all orders that have provided status
    """
    query = Order.query.filter_by(status=status)

    return query
