from uuid import uuid4
from rest_app import db
from rest_app.models.common import Common


class Product(Common, db.Model):
    __tablename__ = 'product'

    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    summary = db.Column(db.Text)
    price = db.Column(db.Numeric(7, 2), nullable=False)
    order_items = db.relationship('OrderItem', backref='product', lazy='dynamic')
    category_id = db.Column(db.ForeignKey('category.id', ondelete='SET NULL'), nullable=False)

    @classmethod
    def create(cls, **kwargs):
        """Creates new product"""
        product = cls(id=str(uuid4()), **kwargs)
        db.session.add(product)
        db.session.commit()
        return product

    def __repr__(self):
        return f'<Product {self.title}>'


# TODO ADD IMAGE ROW HERE