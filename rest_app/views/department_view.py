from flask import Blueprint, render_template
from flask_login import login_required, current_user
from rest_app.views.admin_views import check_if_admin


department = Blueprint('department', __name__, url_prefix='/department')


@department.route('/<string:department_id>')
def department_detail(department_id):
    return f'Hello department{department_id}'


@department.route('/create')
def create_department():
    pass


@department.route('/<string:department_id>/update')
def update_department(department_id):
    pass


@department.route('/<string:department_id>/delete')
def delete_department(department_id):
    pass


@department.before_request
@login_required
def before_admin_request():
    """ Protect all of the admin endpoints. """
    if current_user:
        if not check_if_admin(current_user):
            return 'Unauthorised access'