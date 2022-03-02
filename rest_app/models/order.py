from uuid import uuid4
from sqlalchemy import func
from rest_app import db
from rest_app.models import OrderItem, Product
from rest_app.models.common import Common


class OrderSearch():
    @staticmethod
    def verify_colum_name(col_name):
        if col_name not in ['status', 'total_price', 'order_date', 'order_time']:
            col_name = 'status'

        return col_name

    @classmethod
    def sort_by_total_price(cls, order):
        """Creates a query that sorts a total price column of the Order table in the specified order"""
        subquery = db.session.query(OrderItem.order_id,
                                    func.SUM(Product.price * OrderItem.quantity).label('total_price')) \
            .join(Product) \
            .group_by(OrderItem.order_id).subquery(name='sub')
        query = db.session.query(Order.id, Order.status, Order.order_time, Order.order_date, subquery.c.total_price) \
            .join(subquery, Order.id == subquery.c.order_id) \
            .order_by(order(subquery.c.total_price))

        return query

    @classmethod
    def table_search(cls, query, search):
        """Performs a search on the specific fields of the Order table according to the provided data"""
        query = query.filter(db.or_(
            cls.status.like(f'%{search}%')
        ))

        return query


class Order(Common, OrderSearch, db.Model):
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
