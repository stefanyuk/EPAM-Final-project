from flask import Blueprint, flash, redirect, url_for, render_template
from flask_login import login_required
from rest_app.models import Department, EmployeeInfo
from rest_app.views.admin_views import admin_required
from rest_app.forms.admin_forms import AddEmployee, UpdateEmployee
from rest_app.service.employee_service import employee_form_data_parser, add_employee, update_employee_data
from rest_app.service.common_services import delete_row_by_id


employee = Blueprint('employee', __name__, url_prefix='/employee')


@employee.route('/create', methods=['GET', 'POST'])
def create_employee():
    form = AddEmployee()
    form.department.choices = [department.name for department in Department.query.all()]

    if form.validate_on_submit():
        department_id = Department.query.filter_by(name=form.department.data).first().id
        data = employee_form_data_parser().parse_args()
        add_employee(
            department_id=department_id,
            **data
        )
        flash('Employee was added successfully', 'success')
        return redirect(url_for('admin.admin_main'))

    return render_template('add_employee.html', form=form, title='Create Employee')


@employee.route('/<string:employee_id>/update', methods=['GET', 'POST'])
def update_employee(employee_id):
    form = UpdateEmployee(employee_id)
    form.department.choices = [department.name for department in Department.query.all()]
    form.prepopulate_values()

    if form.validate_on_submit():
        department_id = Department.query.filter_by(name=form.department.data).first().id
        data = employee_form_data_parser().parse_args()
        update_employee_data(
            employee_id=employee_id,
            department_id=department_id,
            **data
        )
        flash('Employee information was successfully updated', 'success')
        return redirect(url_for('admin.admin_main'))

    return render_template(
        'add_employee.html',
        form=form,
        title='Update Employee',
        update=True,
        employee_id=employee_id
    )


@employee.route('/<string:employee_id>/delete')
def delete_employee(employee_id):
    delete_row_by_id(EmployeeInfo, employee_id)
    flash('Employee was successfully deleted', 'success')

    return redirect(url_for('admin.admin_main'))


@employee.before_request
@admin_required
@login_required
def before_admin_request():
    """ Protect all of the admin endpoints. """
