from rest_app import db


class OrderItem(db.Model):
    __tablename__ = 'order_item'

    id = db.Column(db.String, primary_key=True)
    order_id = db.Column(db.ForeignKey('order.id', ondelete='CASCADE'))
    product_id = db.Column(db.ForeignKey('product.id', ondelete='SET NULL'))
