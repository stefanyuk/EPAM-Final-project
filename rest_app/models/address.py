from rest_app import db


class Address(db.Model):
    __tablename__ = 'address'

    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('user.id', ondelete='CASCADE'))
    city = db.Column(db.String, nullable=False)
    street = db.Column(db.String, nullable=False)
    street_number = db.Column(db.String, nullable=False)
    postal_code = db.Column(db.String, nullable=False)
    orders = db.relationship('Order', backref='address', lazy='dynamic')

    def data_to_dict(self):
        """
        Returns address information
        """
        address_info = {
            'id': self.id,
            'city': self.city,
            'street': self.street,
            'street_number': self.street_number,
            'postal_code': self.postal_code
        }

        return address_info

    def __repr__(self):
        return '<Address {}>'.format(self.id)
