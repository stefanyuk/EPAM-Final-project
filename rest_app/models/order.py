from rest_app import db


class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.String, primary_key=True)
    status = db.Column(db.String(20))
    order_date = db.Column(db.Date)
    comments = db.Column(db.Text)
    total_price = db.Column(db.Numeric(10, 3))
    order_time = db.Column(db.Time)
    user_id = db.Column(db.ForeignKey('user.id', ondelete='SET NULL'))
    address_id = db.Column(db.ForeignKey('address.id', ondelete='SET NULL'))
    order_items = db.relationship('OrderItem', backref='order', passive_deletes=True)

    def data_to_dict(self):
        """
        Serializer that returns a dictionary from order table fields
        """
        order_data = {
            'id': self.id,
            'status': self.status,
            'order_date': str(self.order_date),
            'order_time': str(self.order_time)[:8],
            'user_id': self.user_id,
            'total_price': float(self.total_price),
            'order_items': [order_item.product.title for order_item in self.order_items]
        }

        return order_data

    def __repr__(self):
        return f'<Order {self.id}>'
