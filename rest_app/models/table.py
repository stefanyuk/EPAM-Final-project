from rest_app import db


class Table(db.Model):
    __tablename__ = 'table'

    id = db.Column(db.String, primary_key=True)
    capacity = db.Column(db.Integer)
    bookings = db.relationship('Booking', backref='table', lazy='dynamic')
