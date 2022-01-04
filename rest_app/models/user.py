from rest_app import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    registered_at = db.Column(db.Date)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String)
    phone_number = db.Column(db.String)
    last_login_date = db.Column(db.Date)
    birth_date = db.Column(db.Date)
    gender = db.Column(db.String())
    is_admin = db.Column(db.Boolean)
    is_employee = db.Column(db.Boolean)
    addresses = db.relationship('Address', backref='user', lazy='dynamic', passive_deletes=True)
    orders = db.relationship('Order', backref='user', lazy='dynamic')
    employee = db.relationship('EmployeeInfo', backref='user', uselist=False, passive_deletes=True)
    bookings = db.relationship('Booking', backref='user', lazy='dynamic')
