from werkzeug.security import generate_password_hash
from sqlalchemy import func, asc, desc
from flask_restful import reqparse
from flask_restful import inputs
from rest_app.models import User, Order
import datetime
from uuid import uuid4
from rest_app import db


def add_user(username, password, first_name, last_name, email, phone_number,
             birth_date, is_admin, is_employee, user_id=None):

    user = User(
        id=user_id if user_id else str(uuid4()),
        username=username if username else str(uuid4())[0:8],
        password_hash=generate_password_hash(password) if password else generate_password_hash('12345lacrema'),
        registered_at=datetime.datetime.now().date(),
        first_name=first_name,
        last_name=last_name,
        email=f"{first_name}.{last_name}@lacrema.com" if is_employee else email,
        phone_number=phone_number,
        birth_date=birth_date,
        is_admin=is_admin,
        is_employee=is_employee
    )

    db.session.add(user)
    db.session.commit()

    return user


def get_total_value(sort_order='acs'):
    """
    Creates a query to obtain information about total value that each user spent
    """
    order = asc if sort_order == 'asc' else desc

    query = db.session.query(User)\
        .join(Order)\
        .group_by(User.id)\
        .order_by(order(func.ROUND(func.SUM(Order.total_price), 3)))

    return query


def get_all_users_by_employee_filter(employee_filter):
    """
    Creates a query for search either all users who are employees, or who are not

    :param employee_filter: filter based on which search will be performed
    """
    query = User.query.filter_by(is_employee=employee_filter)

    return query


def get_all_users_by_is_admin_filter(is_admin_filter):
    """
    Creates a query for search either all users who are admins, or who are not

    :param is_admin_filter: filter based on which search will be performed
    """
    query = User.query.filter_by(is_admin=is_admin_filter)

    return query


def get_total_value_per_user(user_id):
    """

    :param user_id:
    :return:
    """
    total_value = 0
    user = User.query.get(user_id)

    for order in user.orders:
        total_value += order.total_price

    return total_value


def user_data_parser():
    """Creates a parser in order to parse information about user"""

    parser = reqparse.RequestParser()

    parser.add_argument('username', type=str, location=['json', 'form'])
    parser.add_argument('password', type=str, location=['json', 'form'])
    parser.add_argument('first_name',
                        help='you didn\'t provide first name', type=str, location=['json', 'form'])
    parser.add_argument('last_name', type=str,
                        help='you didn\'t provide last name', location=['json', 'form'])
    parser.add_argument('email', type=str, location=['json', 'form'], required=True)
    parser.add_argument('phone_number', type=str, location=['json', 'form'])
    parser.add_argument('birth_date', type=str, location=['json', 'form'])
    parser.add_argument('is_admin', type=inputs.boolean, location=['json', 'form'], default=False)
    parser.add_argument('is_employee', type=inputs.boolean, location=['json', 'form'], default=False)

    return parser


def form_user_data_parser():
    parser = user_data_parser().copy()

    parser.replace_argument('is_admin', type=bool, location='form')
    parser.replace_argument('is_employee', type=bool, location='form')

    for arg in parser.args:
        if arg.required:
            arg.required = False

    return parser


def user_data_to_dict(user):
    user_info = {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'password': user.password_hash,
        'email': user.email,
        'phone_number': user.phone_number,
        'birth_date': str(user.birth_date),
        'is_admin': user.is_admin,
        'is_employee': user.is_employee,
        'total_value': str(get_total_value_per_user(user.id)),
        'registered_on': str(user.registered_at),
        'last_login_date': str(user.last_login_date)
    }

    return user_info


def update_user(user_id, **kwargs):
    """
    Updates an existing user

    :param user_id: unique user id
    """
    user = User.query.get(user_id)

    for key, value in kwargs.items():
        if key in ('is_admin', 'is_employee') and value is False:
            setattr(user, key, value)
        elif value:
            setattr(user, key, value)

    db.session.commit()
