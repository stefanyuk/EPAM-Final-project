from rest_app import db


class Category(db.Model):
    __tablename = 'category'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, unique=True)
    products = db.relationship('Product', backref='category', lazy='dynamic')

    def data_to_dict(self):
        """
        Returns category information
        """
        category_info = {
            'id': self.id,
            'name': self.name
        }

        return category_info

    def __repr__(self):
        return '<Category {}>'.format(self.name)
