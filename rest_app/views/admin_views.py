from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from flask_login import login_required, current_user
from functools import wraps
from rest_app.schemas import *
from rest_app.service.common_services import sort_table_by_field
from rest_app.service.product_service import get_products_by_category
from rest_app.service.common_services import search_table
from rest_app.models import *

admin = Blueprint('admin', __name__, url_prefix='/admin')
employee_schema = EmployeeSchema()
department_schema = DepartmentSchema()
order_schema = OrderSchema()
product_schema = ProductSchema()
user_schema = UserSchema()


@admin.route('/')
def admin_main():
    return render_template('admin_main.html')


@admin.route('/users')
def users_list():
    """Shows list of all users"""
    return render_template('users.html', title='Users Table')


@admin.route('/users_search')
def users_search():
    """Runs a server-side filtering, searching and filtering of the users table"""
    return search_table(User, user_schema)


@admin.route('/departments')
def departments_list():
    """Shows list of departments"""
    return render_template('departments.html', title='Departments Table')


@admin.route('/departments_search', methods=['GET', 'POST'])
def departments_search():
    """Runs a server-side filtering, searching and filtering of the users table"""
    return search_table(Department, department_schema)


@admin.route('/employees')
def employees_list():
    """Shows list of employees"""
    return render_template('employees.html', title='Employees Table')


@admin.route('/employees_search', methods=['GET', 'POST'])
def employees_search():
    """Runs a server-side filtering, searching and filtering of the employees table"""
    return search_table(EmployeeInfo, employee_schema)


@admin.route('/orders')
def orders_list():
    """Shows list of order"""
    return render_template('orders.html', title='Orders Table')


@admin.route('/orders_search', methods=['GET', 'POST'])
def orders_search():
    """Runs a server-side filtering, searching and filtering of the orders table"""
    return search_table(Order, order_schema)


@admin.route('/products')
def products_list():
    """Shows list of products"""
    return render_template('products.html', title='Products Table')


@admin.route('/products_search', methods=['GET', 'POST'])
def products_search():
    """Runs a server-side filtering, searching and filtering of the products table"""
    return search_table(Product, product_schema)


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            return 'Unauthorized access'
        return func(*args, **kwargs)

    return wrapper


def admin_or_user_required(func):
    @wraps(func)
    def wrapper(user_id):
        if current_user.is_authenticated:
            if current_user.is_admin or current_user.id == user_id:
                return func(user_id)
        else:
            return 'You cannot access this page'

    return wrapper


@admin.before_request
@login_required
@admin_required
def protect_admin_requests():
    """ Protect all of the admin endpoints"""
