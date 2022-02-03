from uuid import uuid4
from rest_app import db
from rest_app.models import OrderItem
from rest_app.models.common import Common


class Order(Common, db.Model):
    __tablename__ = 'order'

    id = db.Column(db.String, primary_key=True)
    status = db.Column(db.String(30))
    order_date = db.Column(db.Date)
    comments = db.Column(db.Text)
    order_time = db.Column(db.Time)
    user_id = db.Column(db.ForeignKey('user.id', ondelete='SET NULL'))
    address_id = db.Column(db.ForeignKey('address.id', ondelete='SET NULL'))
    order_items = db.relationship('OrderItem', backref='order')

    @classmethod
    def create(cls, args: dict):
        """Creates new order"""
        order_items = args.pop('order_items')
        order = Order(id=str(uuid4()), **args)
        db.session.add(order)
        db.session.commit()

        OrderItem.create(order_items, order.id)
        return order

    def calculate_total_price(self):
        """Calculates total value of the order"""
        total_price = 0

        for item in self.order_items:
            total_price += item.product.price * item.quantity

        return total_price

    @classmethod
    def update(cls, model_id, data: dict):
        """
        Updates information about order
        :param data: dictionary containing new information about order
        :param model_id: id of the table row that needs to be deleted
        """
        order = cls.query.get(model_id)
        order_items = data.pop('order_items', None)

        for attr, value in data.items():
            setattr(order, attr, value)

        if order_items:
            OrderItem.update(order_items, order.id)

        db.session.commit()
        return order

    def __repr__(self):
        return f'<Order {self.id}>'
