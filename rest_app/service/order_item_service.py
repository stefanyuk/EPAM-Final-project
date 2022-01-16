from rest_app.models import OrderItem, Product
from rest_app import db
from uuid import uuid4


def create_order_items(products: list, order_id, main_key='title'):
    for product in products:
        product_id = product['id'] if main_key == 'id' else Product.query.filter_by(title=product['title']).first().id
        order_item = OrderItem(
            id=str(uuid4()),
            order_id=order_id,
            product_id=product_id,
            quantity=product['quantity']
        )

        db.session.add(order_item)
        db.session.commit()


def update_order_items(products: list, order_id):
    order_items = db.session.query(OrderItem).filter(OrderItem.order_id == order_id).all()

    for item in order_items:
        db.session.delete(item)

    db.session.commit()

    create_order_items(products, order_id)
