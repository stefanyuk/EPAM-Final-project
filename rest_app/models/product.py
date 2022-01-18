from rest_app import db


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    summary = db.Column(db.Text)
    price = db.Column(db.Numeric(7, 2), nullable=False)
    order_items = db.relationship('OrderItem', backref='product', lazy='dynamic')
    category_id = db.Column(db.ForeignKey('category.id', ondelete='SET NULL'), nullable=False)

    def data_to_dict(self):
        """
        Serializer that returns a dictionary from product table fields
        """
        product_info = {
            'id': self.id,
            'title': self.title,
            'price': str(self.price),
            'category': self.category.name
        }

        return product_info

    def __repr__(self):
        return f'<Product {self.name}>'


# TODO ADD IMAGE ROW HERE