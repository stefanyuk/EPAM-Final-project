from uuid import uuid4
from rest_app import db
from rest_app.models.common import Common


class Address(Common, db.Model):
    __tablename__ = 'address'

    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    city = db.Column(db.String, nullable=False)
    street = db.Column(db.String, nullable=False)
    street_number = db.Column(db.Integer, nullable=False)
    postal_code = db.Column(db.String, nullable=False)
    orders = db.relationship('Order', backref='address', lazy='dynamic')

    @classmethod
    def create(cls, **kwargs):
        """Creates new address"""
        address = cls(id=str(uuid4()), **kwargs)
        db.session.add(address)
        db.session.commit()
        return address

    def __repr__(self):
        return '<Address {}>'.format(self.id)
