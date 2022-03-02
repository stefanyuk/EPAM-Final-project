from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from rest_app.models import Department
from rest_app.views.admin_views import admin_required
from rest_app.forms.admin_forms import AddDepartment, UpdateDepartment
from rest_app.schemas import DepartmentSchema


department = Blueprint('department', __name__, url_prefix='/department')
department_schema = DepartmentSchema()


@department.route('/create', methods=['GET', 'POST'])
def create_department():
    """Creates new department"""
    form = AddDepartment()

    if form.validate_on_submit():
        data = department_schema.dump(form.data)
        Department.create(**data)
        flash('Department was successfully created', 'success')
        return redirect(url_for('admin.admin_main'))
    return render_template('add_department.html', form=form)


@department.route('/<string:department_id>/update', methods=['GET', 'POST'])
def update_department(department_id):
    """Updates specified department"""
    form = UpdateDepartment(department_id)

    if form.validate_on_submit():
        data = department_schema.dump(form.data)
        Department.update(department_id, data)
        flash('Department was successfully updated', 'success')
        return redirect(url_for('admin.admin_main'))

    form.prepopulate_values()

    return render_template('add_department.html', form=form, department_id=department_id, del_btn=True, update=True)


@department.route('/<string:department_id>/delete')
def delete_department(department_id):
    """Deletes specified department"""
    Department.delete(department_id)
    flash('Department was successfully deleted', 'success')
    return redirect(url_for('admin.admin_main'))


@department.before_request
@admin_required
@login_required
def before_admin_request():
    """ Protect all of the department endpoints. """
