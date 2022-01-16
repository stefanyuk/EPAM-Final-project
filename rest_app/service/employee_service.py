from flask_restful import inputs
import datetime
from uuid import uuid4
from rest_app import db
from rest_app.models import EmployeeInfo, Department, User
from rest_app.service.user_service import add_user, user_data_parser
from rest_app.service.common_services import get_row_by_id


def add_employee(first_name, last_name, salary, phone_number, department_id, hire_date, birth_date,
                 is_admin, is_employee, email, password, available_holidays, username=None, user_id=None):
    """
    Creates new employee record in the database

    :param is_admin: database attribute that specifies user rights
    :param is_employee: database attribute that defines whether a user is employee
    :param department_id: id of the department where employee works
    """
    if not user_id:
        user_id = add_user(username, password, first_name, last_name, email, phone_number,
                        birth_date, is_admin, is_employee).id

    employee = EmployeeInfo(
        id=user_id if user_id else str(uuid4()),
        hire_date=hire_date,
        department_id=department_id,
        salary=salary,
        user_id=user_id,
        available_holidays=available_holidays
    )

    db.session.add(employee)
    db.session.commit()

    return employee


def employee_data_to_dict(employee):
    """
    Serializer that returns a dictionary from its fields

    :param employee: employee object that needs to be serialized
    :return: employee information
    """

    employee_info = {
        'first_name': employee.user.first_name,
        'last_name': employee.user.last_name,
        'id': employee.id,
        'hire_date': str(employee.hire_date),
        'department_name': employee.department.name,
        'salary': str(employee.salary),
        'available_holidays': employee.available_holidays
    }

    return employee_info


def update_employee_data(employee_id, **kwargs):
    """
    Update an existing employee

    :param employee_id: unique employee identifier
    """
    employee = get_row_by_id(EmployeeInfo, employee_id)
    user = employee.user

    user_fields = {k: v for k, v in kwargs.items() if k in User.__table__.columns.keys()}
    employee_data_fields = {k: v for k, v in kwargs.items() if k in EmployeeInfo.__table__.columns.keys()}

    for key, value in user_fields.items():
        if value:
            setattr(user, key, value)

    for key, value in employee_data_fields.items():
        if value:
            setattr(employee, key, value)

    db.session.commit()


def employee_data_parser():
    """
    Creates a parser in order to parse information
    provided by user for employee creation
    """
    parser = user_data_parser().copy()

    parser.replace_argument('is_employee', type=inputs.boolean, default=True)
    parser.add_argument('hire_date', type=str, location=['form', 'json'], default=datetime.datetime.now().date())
    parser.add_argument('salary', type=float, location=['form', 'json'],
                        help='you did not provide salary', required=True)
    parser.add_argument('available_holidays', location=['form', 'json'], type=int)
    parser.add_argument('department_id', location=['form', 'json'], type=str,
                        help='you did not provide department id', required=True)

    return parser


def employee_form_data_parser():
    """
    Creates a parser to parse information from the form
    :return:
    """
    parser = employee_data_parser().copy()

    parser.replace_argument('is_admin', type=bool, location='form')
    parser.replace_argument('is_employee', type=bool, location='form', default=True)
    parser.remove_argument('department_id')

    for arg in parser.args:
        if arg.required:
            arg.required = False

    return parser


def get_all_employees_by_department(department_name):
    """
    Creates a query that searches for all employees who belong to the provided department

    :param department_name: name of the department
    """
    dept = Department.query.filter_by(name=department_name).first()
    query = EmployeeInfo.query.filter_by(department_id=dept.id)

    return query
