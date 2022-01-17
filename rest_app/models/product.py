from rest_app import db


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    summary = db.Column(db.Text)
    price = db.Column(db.Numeric(7, 2), nullable=False)
    order_items = db.relationship('OrderItem', backref='product', lazy='dynamic')
    category_id = db.Column(db.ForeignKey('category.id', ondelete='SET NULL'), nullable=False)


# TODO ADD IMAGE ROW HERE