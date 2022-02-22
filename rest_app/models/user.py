import datetime as dt
from flask import request
from sqlalchemy import func, desc, asc
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
from rest_app import db, login_manager
from flask_login import UserMixin
from rest_app.models import Token, Product, OrderItem, Order
from rest_app.models.common import Common


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(Common, db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    registered_on = db.Column(db.Date)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String)
    last_login_date = db.Column(db.Date)
    birth_date = db.Column(db.Date)
    is_admin = db.Column(db.Boolean)
    is_employee = db.Column(db.Boolean)
    addresses = db.relationship('Address', backref='user', lazy='dynamic', cascade="all, delete", passive_deletes=True)
    orders = db.relationship('Order', backref='user', lazy='dynamic')
    employee = db.relationship(
        'EmployeeInfo', backref='user', uselist=False, cascade="all, delete", passive_deletes=True
    )
    token = db.relationship('Token', backref='user', lazy='dynamic', cascade="all, delete", passive_deletes=True)

    @classmethod
    def create(cls, **kwargs):
        """Creates a new user"""
        user = cls(
            id=str(uuid4()) if not kwargs.get('id') else kwargs.pop('id'),
            **kwargs
        )
        db.session.add(user)
        db.session.commit()

        return user

    def update_last_login_date(self):
        """Updates last login date of the user"""
        self.last_login_date = dt.datetime.now().date()
        db.session.commit()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """Verifies whether provided password is correct"""
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self):
        """Generates new authentication token and assigns it to the user"""
        token = Token(user_id=self.id, id=str(uuid4()))
        token.generate()
        return token

    @staticmethod
    def verify_access_token(access_token):
        """Verifies whether provided token exists and if it is still valid"""
        token = Token.query.filter_by(access_token=access_token).first()
        if token:
            if token.access_expiration > dt.datetime.utcnow():
                return token.user

    def total_value(self):
        total_value = 0

        for order in self.orders:
            total_value += order.calculate_total_price()

        return total_value

    @classmethod
    def table_search(cls, query, search):
        """Performs a search on the specific fields of the User table according to the provided data"""
        query = query.filter(db.or_(
            User.username.like(f'%{search}%'),
            User.first_name.like(f'%{search}%'),
            User.last_name.like(f'%{search}%'),
            User.email.like(f'%{search}%')
        ))

        return query

    @staticmethod
    def verify_colum_name(col_name):
        if col_name not in ['username', 'first_name', 'last_name', 'last_login_date', 'is_employee', 'total_value']:
            col_name = 'username'

        return col_name

    @classmethod
    def sort_by_column(cls):
        order = []
        i = 0
        while True:
            col_index = request.args.get(f'order[{i}][column]')
            if col_index is None:
                break
            col_name = cls.verify_colum_name(request.args.get(f'columns[{col_index}][data]'))
            if col_name == 'total_value':
                return cls.sort_by_total_value(i)
            descending = request.args.get(f'order[{i}][dir]') == 'desc'
            col = getattr(cls, col_name)
            if descending:
                col = col.desc()
            order.append(col)
            i += 1

        return order

    @classmethod
    def sort_by_total_value(cls, index):
        order = desc if request.args.get(f'order[{index}][dir]') == 'desc' else asc
        subquery = db.session.query(User.id.label('user_id'), func.sum(Product.price * OrderItem.quantity) \
                                    .label('total_value')) \
            .join(Order) \
            .join(OrderItem) \
            .join(Product) \
            .group_by(User.id).subquery(name='sub')
        query = db.session.query(
            User.id, User.username, User.first_name, User.last_name, User.last_login_date,
            User.phone_number, User.is_employee, subquery.c.total_value
        ) \
            .join(subquery, User.id == subquery.c.user_id) \
            .order_by(order(subquery.c.total_value))
        return query

    def __repr__(self):
        return f'<User {self.username}>'
