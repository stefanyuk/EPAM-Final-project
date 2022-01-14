from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import asc, desc
from functools import wraps
from rest_app.service.department_service import department_data_to_dict, get_average_salary, get_total_employees
from rest_app.service.employee_service import employee_data_to_dict
from rest_app.service.order_service import order_data_to_dict
from rest_app.service.product_service import product_data_to_dict
from rest_app.service.user_service import user_data_to_dict
from rest_app.models import *

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
def admin_main():
    return render_template('admin_main.html')


department_table_filter = {
    'avg_salary': get_average_salary,
    'total_emp': get_total_employees,
}


@admin.route('/departments')
def departments_list():
    return render_template('departments.html')


@admin.route('/department_data')
def department_data():
    return {'data': [department_data_to_dict(department) for department in Department.query]}


@admin.route('/employees')
def employees_list():
    return render_template('employees.html')


@admin.route('/employee_data')
def employee_data():
    return {'data': [employee_data_to_dict(employee) for employee in EmployeeInfo.query]}


@admin.route('/orders')
def orders_list():
    page = request.args.get('page', 1, type=int)
    orders_pagination = Order.query.order_by(Order.order_date.desc(), Order.order_time.desc()) \
        .paginate(page=page, per_page=10)

    orders_info = [order_data_to_dict(order) for order in orders_pagination.items]

    return render_template(
        'orders.html',
        orders=orders_info,
        orders_pagination=orders_pagination
    )


@admin.route('/products')
def products_list():
    page = request.args.get('page', 1, type=int)
    products_pagination = Product.query.paginate(page=page, per_page=10)

    products_info = [product_data_to_dict(product) for product in products_pagination.items]

    return render_template(
        'products.html',
        products=products_info,
        products_pagination=products_pagination
    )


@admin.route('/users')
def users_list():
    page = request.args.get('page', 1, type=int)
    users_pagination = User.query.paginate(page=page, per_page=10)

    users_info = [user_data_to_dict(user) for user in users_pagination.items]

    return render_template(
        'users.html',
        users=users_info,
        users_pagination=users_pagination
    )

# TODO CHECK HOW TO ADD INDEX TO THE TABLE IF DON'T KNOW DELETE ROW NUMBER


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            return 'Unauthorized access'
        return func(*args, **kwargs)
    return wrapper


@admin.before_request
@login_required
@admin_required
def before_admin_request():
    """ Protect all of the admin endpoints. """


def admin_or_user_required(func):
    @wraps(func)
    def wrapper(user_id):
        if current_user.is_authenticated:
            if current_user.is_admin or current_user.id == user_id:
                return func(user_id)
        else:
            return 'You cannot access this page'
    return wrapper
