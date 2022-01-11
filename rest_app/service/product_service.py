from rest_app.models import Product, Category
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


def get_all_products():
    """
    Gathers all the information about each product that is in the database.
    And prepares it for display on the page
    """
    info_about_products = []

    for category in Category.query.all():
        for product in category.products:
            info_about_products.append(
                product_data_to_dict(product)
            )

    return info_about_products
