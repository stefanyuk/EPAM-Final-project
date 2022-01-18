from flask_restful import reqparse
from uuid import uuid4
from datetime import datetime
from rest_app import db
from rest_app.service.order_item_service import update_order_items
from rest_app.service.common_services import get_row_by_id, set_all_parser_args_to_unrequired
from rest_app.models import Order, Product


def get_order_products_total_price(products: list, main_key):
    """
    Returns a total price of ordered products

    :param products: products ordered by a client
    :param main_key: key according to which products search will be performed
    """
    total_price = 0

    for product in products:
        new_product = Product.query.get(product['id']) if main_key == 'id' else Product.query.filter_by(
            title=product['title']).first()
        total_price += new_product.price * product['quantity']

    return total_price


def create_order(products: list, user_id, main_key, address_id, comments=None, status=None):
    """
    Creates new order in the database

    :param products: products ordered by a client
    :param comments: comments that customer left for this order
    :param user_id: unique id of a customer
    :param status: status of the order
    :param address_id: address where order needs to be delivered
    :param main_key: address where order needs to be delivered
    """

    order = Order(
        id=str(uuid4()),
        status=status if status else 'awaiting fulfilment',
        order_date=datetime.now().date(),
        comments=comments,
        user_id=user_id,
        order_time=datetime.now().time(),
        total_price=get_order_products_total_price(products, main_key),
        address_id=address_id
    )

    db.session.add(order)
    db.session.commit()

    return order


def verify_products(products, main_key):
    """
    Verifies whether user provided correct product data

    :param products: list of product names
    :param main_key: key according to which search will be performed
    """
    products_not_found = []

    for attr in products:
        if main_key == 'title':
            product = Product.query.filter_by(title=attr['title']).first()
        else:
            product = Product.query.get(attr['id'])

        if not product:
            products_not_found.append(attr)

    return products_not_found


def update_order(order_id, main_key, **kwargs):
    """
    Update information about existing order

    :param order_id: unique id of the order
    :param main_key: according to which products search will be performed
    """

    order = get_row_by_id(Order, order_id)
    items_except_products = {k: v for k, v in kwargs.items() if k != 'products'}

    if products := kwargs.get('products'):
        update_order_items(products, order.id, main_key)

    for key, value in items_except_products.items():
        if value:
            setattr(order, key, value)

    db.session.commit()


def create_order_data_parser():
    """
    Creates parser to parse information needed for order creation
    """
    parser = reqparse.RequestParser()

    parser.add_argument('comments', type=str)
    parser.add_argument('user_id', type=str, location='json', help='you did not provide user id', required=True)
    parser.add_argument('address_id', type=str, location='json', help='you did not provide address id', required=True)
    parser.add_argument('products', type=str, location='json',
                        action='append', help='you did not provide products', required=True)

    return parser


def update_order_data_parser():
    """
    Creates parser to parse information that user wants to update
    """
    parser = create_order_data_parser().copy()
    parser.add_argument('status', type=str, help='status of the order')

    return set_all_parser_args_to_unrequired(parser)


def get_orders_by_status(status):
    """
    Creates a query to obtain all orders that have provided status
    """
    query = Order.query.filter_by(status=status)

    return query
