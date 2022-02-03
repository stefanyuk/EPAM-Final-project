from uuid import uuid4
from rest_app import db
from rest_app.models import Product
from rest_app.models.common import Common


class OrderItem(Common, db.Model):
    __tablename__ = 'order_item'

    id = db.Column(db.String, primary_key=True)
    order_id = db.Column(db.ForeignKey('order.id', ondelete='CASCADE'))
    product_id = db.Column(db.ForeignKey('product.id', ondelete='SET NULL'))
    quantity = db.Column(db.Integer)

    @classmethod
    def create(cls, order_items: dict, order_id):
        """
        Creates order items of the specified order in the database

        :param order_items: items that were added to the order
        :param order_id: id of the order
        """
        for info in order_items:
            product = Product.query.get(info['product_id'])
            order_item = cls(id=str(uuid4()), order_id=order_id, product_id=product.id, quantity=info['quantity'])
            db.session.add(order_item)

        db.session.commit()

    @classmethod
    def update(cls, order_items, order_id):
        """
        Updates all order items for the specified order
        :param order_items: new order items that should be assigned to the order
        :param order_id: unique id of the order
        """
        old_order_items = cls.query.filter_by(order_id=order_id).all()

        for item in old_order_items:
            db.session.delete(item)

        db.session.commit()
        cls.create(order_items, order_id)

    def __repr__(self):
        return f'<Order Item {self.id}>'
