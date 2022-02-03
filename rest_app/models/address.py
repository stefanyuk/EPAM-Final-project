from uuid import uuid4
from rest_app import db
from rest_app.models.common import Common


class Address(Common, db.Model):
    __tablename__ = 'address'

    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('user.id', ondelete='CASCADE'))
    city = db.Column(db.String, nullable=False)
    street = db.Column(db.String, nullable=False)
    street_number = db.Column(db.String, nullable=False)
    postal_code = db.Column(db.String, nullable=False)
    orders = db.relationship('Order', backref='address', lazy='dynamic')

    @classmethod
    def create(cls, **kwargs):
        """Creates new address"""
        return cls(id=str(uuid4()), **kwargs)

    def __repr__(self):
        return '<Address {}>'.format(self.id)
