from flask import Blueprint, render_template
from flask_login import login_required, current_user
from rest_app.views.admin_views import check_if_admin


employee = Blueprint('employee', __name__, url_prefix='/employee')


@employee.route('/<string:employee_id>')
def employee_detail(employee_id):
    pass


@employee.route('/create')
def create_employee():
    pass


@employee.route('/<string:employee_id>/update')
def update_employee(employee_id):
    pass


@employee.route('/<string:employee_id>/delete')
def delete_employee(employee_id):
    pass



@employee.before_request
@login_required
def before_admin_request():
    """ Protect all of the admin endpoints. """
    if current_user:
        if not check_if_admin(current_user):
            return 'Unauthorised access'