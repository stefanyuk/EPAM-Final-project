from rest_app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    registered_at = db.Column(db.Date)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String)
    last_login_date = db.Column(db.Date)
    birth_date = db.Column(db.Date)
    is_admin = db.Column(db.Boolean)
    is_employee = db.Column(db.Boolean)
    addresses = db.relationship('Address', backref='user', lazy='dynamic', passive_deletes=True)
    orders = db.relationship('Order', backref='user', lazy='dynamic')
    employee = db.relationship('EmployeeInfo', backref='user', uselist=False, passive_deletes=True)

    def __repr__(self):
        return f'<User {self.username}>'
