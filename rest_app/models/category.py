from uuid import uuid4
from rest_app import db
from rest_app.models.common import Common


class Category(Common, db.Model):
    __tablename = 'category'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, unique=True)
    products = db.relationship('Product', backref='category', lazy='dynamic')

    @classmethod
    def create(cls, **kwargs):
        """Create new category"""
        return cls(id=str(uuid4()), **kwargs)

    def __repr__(self):
        return '<Category {}>'.format(self.name)
