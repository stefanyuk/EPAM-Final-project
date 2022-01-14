from werkzeug.security import generate_password_hash
from flask_restful import reqparse
from flask_restful import inputs
from rest_app.models import User
import datetime
from uuid import uuid4
from rest_app import db
from rest_app.service.common_services import get_row_by_id


def add_user(username, password, first_name, last_name, email, phone_number, gender,
             birth_date, is_admin, is_employee):

    user = User(
        id=str(uuid4()),
        username=username if username else str(uuid4())[0:8],
        password_hash=generate_password_hash(password) if password else generate_password_hash('12345lacrema'),
        registered_at=datetime.datetime.now().date(),
        first_name=first_name,
        last_name=last_name,
        email=f"{first_name}.{last_name}@lacrema.com" if is_employee else email,
        phone_number=phone_number,
        birth_date=birth_date,
        gender=gender,
        is_admin=is_admin,
        is_employee=is_employee
    )

    db.session.add(user)
    db.session.commit()

    return user


def get_total_value_spent_in_the_restaurant(user_id):
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
    parser.add_argument('gender', type=str, location=['json', 'form'])
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
        'gender': user.gender,
        'is_admin': user.is_admin,
        'is_employee': user.is_employee,
        'total_value': str(get_total_value_spent_in_the_restaurant(user.id)),
        'registered_on': str(user.registered_at),
        'last_login_date': str(user.last_login_date)
    }

    return user_info


def update_user(user_id, **kwargs):
    """
    Updates an existing user

    :param user_id: unique user id
    """
    user = get_row_by_id(User, user_id)

    for key, value in kwargs.items():
        if key in ('is_admin', 'is_employee') and value is False:
            setattr(user, key, value)
        elif value:
            setattr(user, key, value)

    db.session.commit()
