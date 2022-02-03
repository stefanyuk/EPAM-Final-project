from flask import Blueprint, flash, redirect, url_for, render_template
from marshmallow import EXCLUDE
from flask_login import login_required
from rest_app.models import Department, EmployeeInfo
from rest_app.views.admin_views import admin_required
from rest_app.forms.admin_forms import AddEmployee, UpdateEmployee
from rest_app.schemas import EmployeeSchema, EmployeeCreateSchema


employee = Blueprint('employee', __name__, url_prefix='/employee')
employee_schema = EmployeeSchema(partial=True, unknown=EXCLUDE)
employee_create_schema = EmployeeCreateSchema(partial=True, unknown=EXCLUDE)


@employee.route('/create', methods=['GET', 'POST'])
def create_employee():
    """Creates new employee"""
    form = AddEmployee()
    form.department.choices = [department.name for department in Department.query.all()]

    if form.validate_on_submit():
        data = employee_create_schema.load(form.data)
        EmployeeInfo.create(**data)
        flash('Employee was added successfully', 'success')
        return redirect(url_for('admin.admin_main'))

    return render_template('add_employee.html', form=form, title='Create Employee')


@employee.route('/<string:employee_id>/update', methods=['GET', 'POST'])
def update_employee(employee_id):
    """Updates specified employee"""
    form = UpdateEmployee(employee_id)
    form.department.choices = [department.name for department in Department.query.all()]

    if form.validate_on_submit():
        data = employee_schema.load(form.data)
        EmployeeInfo.update(employee_id, data)
        flash('Employee information was successfully updated', 'success')
        return redirect(url_for('admin.admin_main'))

    form.prepopulate_values()
    return render_template(
        'add_employee.html',
        form=form,
        title='Update Employee',
        update=True,
        employee_id=employee_id,
        del_btn=True
    )


@employee.route('/<string:employee_id>/delete')
def delete_employee(employee_id):
    """Deletes specified employee"""
    EmployeeInfo.delete(employee_id)
    flash('Employee was successfully deleted', 'success')

    return redirect(url_for('admin.admin_main'))


@employee.before_request
@admin_required
@login_required
def before_admin_request():
    """ Protect all of the admin endpoints. """
