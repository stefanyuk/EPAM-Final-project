from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from rest_app.views.admin_views import admin_required
from rest_app.forms.admin_forms import AddDepartment, UpdateDepartment
from rest_app.service.department_service import add_department, department_form_data_parser, update_department_data


department = Blueprint('department', __name__, url_prefix='/department')


@department.route('/create', methods=['GET', 'POST'])
def create_department():
    form = AddDepartment()

    if form.validate_on_submit():
        data = department_form_data_parser().parse_args()
        add_department(**data)
        flash('Department was successfully created', 'success')
        return redirect(url_for('admin.admin_main'))
    return render_template('add_department.html', form=form)


@department.route('/<string:department_id>/update', methods=['GET', 'POST'])
def update_department(department_id):
    form = UpdateDepartment(department_id)
    form.prepopulate_values()

    if form.validate_on_submit():
        data = department_form_data_parser().parse_args()
        update_department_data(department_id, **data)
        flash('Department was successfully updated', 'success')
        return redirect(url_for('admin.admin_main'))

    return render_template('add_department.html', form=form)


@department.route('/<string:department_id>/delete')
def delete_department(department_id):
    pass


@department.before_request
@admin_required
@login_required
def before_admin_request():
    """ Protect all of the department endpoints. """
