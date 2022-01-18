from rest_app import db


class Category(db.Model):
    __tablename = 'category'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, unique=True)
    products = db.relationship('Product', backref='category', lazy='dynamic')
