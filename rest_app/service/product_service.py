from rest_app.models import Product
from uuid import uuid4


def add_product(title, summary, price):
    """
    Creates a new product in the database

    :param title: title of the new product
    :param summary: product description
    :param price: product price
    """
    Product.create(
        public_id=str(uuid4()),
        title=title,
        summary=summary,
        price=price
    )
