from rest_app import db


class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.String, primary_key=True)
    status = db.Column(db.String(20))
    order_date = db.Column(db.Date)
    comments = db.Column(db.Text)
    total_price = db.Column(db.Numeric(10, 3))
    order_time = db.Column(db.Time)
    user_id = db.Column(db.ForeignKey('user.id', ondelete='SET NULL'), nullable=False)
    address_id = db.Column(db.ForeignKey('address.id', ondelete='SET NULL'), nullable=False)
    order_items = db.relationship('OrderItem', backref='order', passive_deletes=True)
