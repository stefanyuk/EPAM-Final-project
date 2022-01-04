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
