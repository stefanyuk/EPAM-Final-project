from sqlalchemy import func, asc, desc
from flask_restful import reqparse
from flask_restful import inputs
from rest_app.models import User, Order
from rest_app import db
from rest_app.service.common_services import get_row_by_id, set_all_parser_args_to_unrequired


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


def update_user_data_parser():
    """
    Creates a parser that can be used to update user data from json body
    """
    parser = user_data_parser().copy()

    return set_all_parser_args_to_unrequired(parser)


def form_user_data_parser():
    """
    Creates a parser that can be used to parse information from web form
    """
    parser = update_user_data_parser().copy()

    parser.replace_argument('is_admin', type=bool, location='form')
    parser.replace_argument('is_employee', type=bool, location='form')

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
        'registered_on': str(user.registered_on),
        'last_login_date': str(user.last_login_date),
        'address_id': user.addresses.all()[-1].id if user.addresses.all() else None
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
