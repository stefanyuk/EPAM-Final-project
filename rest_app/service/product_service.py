from flask_restful import reqparse
from rest_app.models import Product, Category
from rest_app.service.common_services import get_row_by_id, set_all_parser_args_to_unrequired
from rest_app import db
from uuid import uuid4


def add_product(title, summary, price, category_id):
    """
    Creates a new product in the database

    :param title: title of the new product
    :param summary: product description
    :param price: product price
    :param category_id: category of the product
    """
    product = Product(
        id=str(uuid4()),
        title=title,
        summary=summary,
        price=price,
        category_id=category_id
    )

    db.session.add(product)
    db.session.commit()

    return product


def product_data_to_dict(product):
    """
    Serializer that returns a dictionary from its fields

    :param product: product object that needs to be serialized
    :return: product information
    """
    product_info = {
        'id': product.id,
        'title': product.title,
        'price': product.price,
        'category': product.category.name
    }

    return product_info


def get_products_by_category(category_name):
    """
    Select all records for the products that are under provided category

    :param category_name: name of the searched category
    """
    category = Category.query.filter_by(name=category_name).first()
    products = Product.query.filter_by(category_id=category.id)

    return products


def product_data_parser():
    parser = reqparse.RequestParser()

    parser.add_argument('title', type=str, help='you did not provide product title', required=True)
    parser.add_argument('price', type=float, help='you did not provide product price', required=True)
    parser.add_argument('category_id', type=str, help='you did not provide product category id', required=True)
    parser.add_argument('summary', type=str, help='you did not provide product title')

    return parser


def product_update_data_parser():
    parser = product_data_parser().copy()

    return set_all_parser_args_to_unrequired(parser)


def update_product(product_id, **kwargs):
    """
    Updates information about specified product
    :param product_id: unique product id
    """
    product = get_row_by_id(Product, product_id)

    for field in kwargs:
        if kwargs[field]:
            setattr(product, field, kwargs[field])

    db.session.commit()
