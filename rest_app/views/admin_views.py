from flask import Blueprint, render_template, request, session, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import asc, desc
from functools import wraps
from rest_app.service.department_service import department_data_to_dict, get_average_salary, get_total_employees
from rest_app.service.employee_service import employee_data_to_dict, get_all_employees_by_department
from rest_app.service.order_service import order_data_to_dict
from rest_app.service.product_service import product_data_to_dict, get_products_by_category
from rest_app.service.user_service import user_data_to_dict, get_total_value_per_user, get_all_users_by_employee_filter
from rest_app.models import *
from rest_app.forms.admin_forms import FilterProductsForm, FilterEmployeesForm, FilterUserForm

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
    page, index = get_index_and_page_number()
    form = FilterEmployeesForm()
    form.populate_choices_fields()
    employees_pagination = EmployeeInfo.query.paginate(page=page, per_page=10)
    employees_info = [employee_data_to_dict(employee) for employee in employees_pagination.items]

    return render_template(
        'employees.html',
        employees=employees_info,
        employees_pagination=employees_pagination,
        form=form,
        index=index
    )


@admin.route('employees/search', methods=['GET', 'POST'])
def employees_search():
    page, index = get_index_and_page_number()
    form = FilterEmployeesForm()
    form.populate_choices_fields()

    if form.validate_on_submit():
        session['employees_search'] = True
        session['search_filter'] = form.filter_option.data
        session['sort_order'] = form.order.data
        session['field_name'] = form.field_name.data
        session['department_name'] = form.department.data

    if session.get('employees_search'):
        if session['search_filter'] == 'Search by':
            dept_name = session.get('department_name')
            employees_pagination = get_all_employees_by_department(dept_name).paginate(page=page, per_page=10)
        else:
            employees_pagination = EmployeeInfo.query.order_by(order[session['sort_order']](session['field_name']))\
                .paginate(page=page, per_page=10)
    else:
        return redirect(url_for('admin.employees_list'))

    employees_info = [employee_data_to_dict(employee) for employee in employees_pagination.items]

    return render_template(
        'employees.html',
        employees=employees_info,
        employees_pagination=employees_pagination,
        form=form
    )


@admin.route('/orders')
def orders_list():
    page = request.args.get('page', 1, type=int)
    orders_pagination = Order.query.order_by(desc(Order.order_date), desc(Order.order_time)) \
        .paginate(page=page, per_page=10)

    orders_info = [order_data_to_dict(order) for order in orders_pagination.items]

    return render_template(
        'orders.html',
        orders=orders_info,
        orders_pagination=orders_pagination
    )


@admin.route('/products')
def products_list():
    page, index = get_index_and_page_number()
    form = FilterProductsForm()
    form.populate_choices_fields()
    products_pagination = Product.query.paginate(page=page, per_page=10)
    products_info = [product_data_to_dict(product) for product in products_pagination.items]

    return render_template(
        'products.html',
        products=products_info,
        products_pagination=products_pagination,
        form=form,
        index=index
    )


@admin.route('products/search', methods=['GET', 'POST'])
def products_search():
    page, index = get_index_and_page_number()
    form = FilterProductsForm()
    form.populate_choices_fields()

    if form.validate_on_submit():
        session['products_search'] = True
        session['search_filter'] = form.filter_option.data
        session['sort_order'] = form.order.data
        session['field_name'] = form.field_name.data
        session['product_search_category'] = form.category.data

    if session.get('products_search'):
        if session['search_filter'] == 'Search by':
            category_name = session.get('product_search_category')
            products_pagination = get_products_by_category(category_name).paginate(page=page, per_page=10)
        else:
            products_pagination = Product.query.order_by(order[session['sort_order']](session['field_name'])).paginate(
                page=page,
                per_page=10)
    else:
        return redirect(url_for('admin.products'))

    products_info = [product_data_to_dict(product) for product in products_pagination.items]

    return render_template(
        'products.html',
        products=products_info,
        products_pagination=products_pagination,
        form=form,
        index=index
    )


@admin.route('/users')
def users_list():
    page, index = get_index_and_page_number()
    form = FilterUserForm()
    form.populate_choices_fields()
    users_pagination = User.query.paginate(page=page, per_page=10)
    users_info = [user_data_to_dict(user) for user in users_pagination.items]

    return render_template(
        'users.html',
        users=users_info,
        users_pagination=users_pagination,
        form=form,
        index=index
    )


@admin.route('users/search', methods=['GET', 'POST'])
def users_search():
    page, index = get_index_and_page_number()
    form = FilterUserForm()
    form.populate_choices_fields()

    if form.validate_on_submit():
        session['users_search'] = True
        session['search_filter'] = form.filter_option.data
        session['sort_order'] = form.order.data
        session['field_name'] = form.field_name.data
        session['is_employee'] = form.is_employee.data

    if session.get('users_search'):
        if session.get('search_filter') == 'Search by':
            users_pagination = get_all_users_by_employee_filter(session.get('is_employee'))\
                .paginate(page=page, per_page=10)
        else:
            if session.get('field_name') == 'total_money_spent':
                users_pagination = get_total_value_per_user()\
                    .order_by(order[session['sort_order']](session['field_name']))\
                    .paginate(page=page, per_page=10)
            else:
                users_pagination = User.query.order_by(
                    order[session['sort_order']](session['field_name'])).paginate(
                    page=page,
                    per_page=10)
    else:
        return redirect(url_for('admin.users_list'))

    users_info = [user_data_to_dict(user) for user in users_pagination.items]

    return render_template(
        'users.html',
        users=users_info,
        users_pagination=users_pagination,
        form=form,
        index=index
    )


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
def protect_admin_requests():
    """ Protect all of the admin endpoints"""


endpoints_controls = {
    'products_search': 'admin.products_search',
    'employees_search': 'admin.employees_search',
    'users_search': 'admin.users_search'
}


@admin.before_request
def clear_sort_table_session():
    """
    Clears session from sort tables options in case if they are set and admin does not filter anything
    """
    for search_table, route_name in endpoints_controls.items():
        if session.get(search_table):
            if request.endpoint != route_name:
                session[search_table] = False
                break
    session.modified = True


def admin_or_user_required(func):
    @wraps(func)
    def wrapper(user_id):
        if current_user.is_authenticated:
            if current_user.is_admin or current_user.id == user_id:
                return func(user_id)
        else:
            return 'You cannot access this page'

    return wrapper


# We use it in order to sort table in a chosen by user order
order = {
    'asc': asc,
    'desc': desc
}


def get_index_and_page_number():
    """
    Parses information regarding pagination page from the users request and creates row index list
    :return: current pagination page, row index list
    """
    page = request.args.get('page', 1, type=int)
    index = list(range(11)) if page == 1 else list(range((page - 1) * 10, (page * 10) + 1))

    return page, index
