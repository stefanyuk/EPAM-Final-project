from rest_app.models import OrderItem, Product
from rest_app import db
from uuid import uuid4

# TODO THINK HOW TO COMBINE PRODUCTS WITH ID AND PRODUCTS BY NAME

def create_order_items(products: list, order_id):
    for title in products:
        order_item = OrderItem(
            id=str(uuid4()),
            order_id=order_id,
            product_id=db.session.query(Product).filter(Product.title == title).one().id
        )

        db.session.add(order_item)
        db.session.commit()


def update_order_items(products: list, order_id):
    order_items = db.session.query(OrderItem).filter(OrderItem.order_id == order_id).all()

    for item in order_items:
        db.session.delete(item)

    db.session.commit()

    create_order_items(products, order_id)
