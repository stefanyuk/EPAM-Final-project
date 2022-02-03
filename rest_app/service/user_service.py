from sqlalchemy import func, asc, desc
from rest_app.models import User, Order
from rest_app import db


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
