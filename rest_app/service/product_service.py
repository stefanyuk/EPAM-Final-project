from rest_app.models import Product
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
    product = Product.create(
        public_id=str(uuid4()),
        title=title,
        summary=summary,
        price=price,
        category_id=category_id
    )

    db.session.add(product)
    db.session.commit()

    return product.id
