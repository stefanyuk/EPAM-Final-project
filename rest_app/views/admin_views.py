from flask import Blueprint, render_template, request, session, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import desc
from functools import wraps
from rest_app.service.common_services import sort_table_by_field
from rest_app.service.department_service import sort_dept_by_average_salary, sort_dept_by_total_employees
from rest_app.service.employee_service import get_all_employees_by_department
from rest_app.service.order_service import get_orders_by_status
from rest_app.service.product_service import get_products_by_category
from rest_app.service.user_service import user_data_to_dict, get_total_value, get_all_users_by_employee_filter
from rest_app.models import *
from rest_app.forms.admin_forms import FilterProductsForm, FilterEmployeesForm, FilterUsersForm, FilterOrdersForm, \
    FilterDepartmentsForm

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
def admin_main():
    return render_template('admin_main.html')


@admin.route('/departments')
def departments_list():
    page, index = get_row_index_and_page_number()
    form = create_search_form_and_add_choice_fields(FilterDepartmentsForm)
    departments_pagination = Department.query.paginate(page=page, per_page=10)
    departments_info = [department.data_to_dict() for department in departments_pagination.items]

    return render_template(
        'departments.html',
        form=form,
        index=index,
        departments_pagination=departments_pagination,
        departments=departments_info
    )


@admin.route('/departments/search', methods=['GET', 'POST'])
def departments_search():
    page, index = get_row_index_and_page_number()
    form = create_search_form_and_add_choice_fields(FilterDepartmentsForm)
    set_search_form_data_in_session(form, 'departments_search', [form.department])

    if session.get('departments_search'):
        if session.get('search_filter') == 'Search by':
            query = Department.query.filter_by(name=session.get('department'))
        else:
            if session.get('field_name') == 'avg_salary':
                query = sort_dept_by_average_salary(session.get('sort_order'))
            elif session.get('field_name') == 'total_employees':
                query = sort_dept_by_total_employees(session.get('sort_order'))
            else:
                query = sort_table_by_field(Department, session.get('field_name'), session.get('sort_order'))
    else:
        return redirect(url_for('admin.departments_list'))

    departments_pagination = query.paginate(page=page, per_page=10)
    departments_info = [department.data_to_dict() for department in departments_pagination.items]

    return render_template(
        'departments.html',
        form=form,
        index=index,
        departments_pagination=departments_pagination,
        departments=departments_info
    )


@admin.route('/employees')
def employees_list():
    page, index = get_row_index_and_page_number()
    form = create_search_form_and_add_choice_fields(FilterEmployeesForm)
    employees_pagination = EmployeeInfo.query.paginate(page=page, per_page=10)
    employees_info = [employee.data_to_dict() for employee in employees_pagination.items]

    return render_template(
        'employees.html',
        employees=employees_info,
        employees_pagination=employees_pagination,
        form=form,
        index=index
    )


@admin.route('employees/search', methods=['GET', 'POST'])
def employees_search():
    page, index = get_row_index_and_page_number()
    form = create_search_form_and_add_choice_fields(FilterEmployeesForm)
    set_search_form_data_in_session(form, 'employees_search', [form.department])

    if session.get('employees_search'):
        if session['search_filter'] == 'Search by':
            query = get_all_employees_by_department(session.get('department'))
        else:
            query = sort_table_by_field(EmployeeInfo, session.get('field_name'), session.get('sort_order'), User)
    else:
        return redirect(url_for('admin.employees_list'))

    employees_pagination = query.paginate(page=page, per_page=10)
    employees_info = [employee.data_to_dict() for employee in employees_pagination.items]

    return render_template(
        'employees.html',
        employees=employees_info,
        employees_pagination=employees_pagination,
        form=form,
        index=index
    )


@admin.route('/orders')
def orders_list():
    page, index = get_row_index_and_page_number()
    form = create_search_form_and_add_choice_fields(FilterOrdersForm)

    orders_pagination = Order.query.order_by(desc(Order.order_date), desc(Order.order_time)) \
        .paginate(page=page, per_page=10)

    orders_info = [order.data_to_dict() for order in orders_pagination.items]

    return render_template(
        'orders.html',
        orders=orders_info,
        orders_pagination=orders_pagination,
        form=form,
        index=index
    )


@admin.route('orders/search', methods=['GET', 'POST'])
def orders_search():
    page, index = get_row_index_and_page_number()
    form = create_search_form_and_add_choice_fields(FilterOrdersForm)
    set_search_form_data_in_session(form, 'orders_search', [form.status])

    if session.get('orders_search'):
        if session['search_filter'] == 'Search by':
            query = get_orders_by_status(session.get('status'))
        else:
            query = sort_table_by_field(Order, session.get('field_name'), session.get('sort_order'))
    else:
        return redirect(url_for('admin.orders_list'))

    orders_pagination = query.paginate(page=page, per_page=10)
    orders_info = [order.data_to_dict() for order in orders_pagination.items]

    return render_template(
        'orders.html',
        orders=orders_info,
        orders_pagination=orders_pagination,
        form=form,
        index=index
    )


@admin.route('/products')
def products_list():
    page, index = get_row_index_and_page_number()
    form = create_search_form_and_add_choice_fields(FilterProductsForm)

    products_pagination = Product.query.paginate(page=page, per_page=10)
    products_info = [product.data_to_dict() for product in products_pagination.items]

    return render_template(
        'products.html',
        products=products_info,
        products_pagination=products_pagination,
        form=form,
        index=index
    )


@admin.route('products/search', methods=['GET', 'POST'])
def products_search():
    page, index = get_row_index_and_page_number()
    form = create_search_form_and_add_choice_fields(FilterProductsForm)
    set_search_form_data_in_session(form, 'products_search', [form.category])

    if session.get('products_search'):
        if session['search_filter'] == 'Search by':
            query = get_products_by_category(session.get(form.category.name))
        else:
            query = sort_table_by_field(Product, session.get('field_name'), session.get('sort_order'))
    else:
        return redirect(url_for('admin.products_list'))

    products_pagination = query.paginate(page=page, per_page=10)
    products_info = [product.data_to_dict() for product in products_pagination.items]

    return render_template(
        'products.html',
        products=products_info,
        products_pagination=products_pagination,
        form=form,
        index=index
    )


@admin.route('/users')
def users_list():
    page, index = get_row_index_and_page_number()
    form = create_search_form_and_add_choice_fields(FilterUsersForm)
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
    page, index = get_row_index_and_page_number()
    form = create_search_form_and_add_choice_fields(FilterUsersForm)
    set_search_form_data_in_session(form, 'users_search', [form.is_employee])

    if session.get('users_search'):
        if session.get('search_filter') == 'Search by':
            query = get_all_users_by_employee_filter(session.get('is_employee'))
        else:
            if session.get('field_name') == 'total_money_spent':
                query = get_total_value(session.get('sort_order'))
            else:
                query = sort_table_by_field(User, session.get('field_name'), session.get('sort_order'))
    else:
        return redirect(url_for('admin.users_list'))

    users_pagination = query.paginate(page=page, per_page=10)
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


def create_search_form_and_add_choice_fields(form):
    """
    Creates a form and adds all necessary values to choice field

    :param form: form that needs to be created
    :return: form instance
    """
    form_instance = form()
    form_instance.populate_choices_fields()

    return form_instance


def get_row_index_and_page_number():
    """
    Parses information regarding pagination page from the request and creates row index list
    :return: current pagination page, row index list
    """
    page = request.args.get('page', 1, type=int)
    index = list(range(11)) if page == 1 else list(range((page - 1) * 10, (page * 10) + 1))

    return page, index


def set_search_form_data_in_session(form, form_name, form_fields: list = None):
    """
    In case of successful validation, it sets all necessary information for the form in the session,
    so it persists while user is using it and can be used to return the result to the user

    :param form: form that needs to be validated and set in the session
    :param form_name: name that should be used for saving in session
    :param form_fields: not common fields of the form
    """
    if form.validate_on_submit():
        session[form_name] = True
        session['search_filter'] = form.filter_option.data
        session['sort_order'] = form.order.data
        session['field_name'] = form.field_name.data
        if form_fields:
            for field in form_fields:
                session[field.name] = field.data


endpoints_controls = {
    'products_search': 'admin.products_search',
    'employees_search': 'admin.employees_search',
    'users_search': 'admin.users_search',
    'departments_search': 'admin.departments_search'
}


@admin.before_request
def clear_table_search_session():
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


@admin.before_request
@login_required
@admin_required
def protect_admin_requests():
    """ Protect all of the admin endpoints"""
