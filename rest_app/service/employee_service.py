from flask_restful import reqparse

from rest_app.models import EmployeeInfo
from rest_app.service.user_service import add_user, user_data_parser
from rest_app.service.common_services import get_row_by_id
import datetime
from uuid import uuid4
from rest_app import db


def add_employee(salary, department_id, hire_date, available_holidays, user_id):
    """
    Add new employee to the database
    
    :param salary: employee salary
    :param hire_date: date when employee was hired
    :param department_id: id of the department where employee works
    :param available_holidays: amount of employee holidays
    :param user_id: id of the user with which employee is associated
    """

    employee = EmployeeInfo(
        id=str(uuid4()),
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
        'hire_date': employee.hire_date,
        'department_name': employee.department.name,
        'salary': employee.salary,
        'available_holidays': employee.available_holidays
    }

    return employee_info


def update_employee(employee_id, **kwargs):
    """
    Update an existing employee

    :param employee_id: unique employee identifier
    """
    employee = get_row_by_id(EmployeeInfo, employee_id)
    user = employee.user

    user_fields = {k: kwargs[k] for k in list(kwargs)[:10]}
    employee_data_fields = {k: kwargs[k] for k in list(kwargs)[15:]}

    for key, value in user_fields.items():
        if value:
            setattr(user, key, value)

    for key, value in employee_data_fields.items():
        if value:
            setattr(user, key, value)

    db.session.commit()


def employee_data_parser():
    """
    Creates a parser in order to parse information
    provided by user for employee creation
    """
    parser = reqparse.RequestParser()

    parser.add_argument('hire_date', type=str, default=datetime.datetime.now().date())
    parser.add_argument('salary', type=float, help='you did not provide employee salary', required=True)
    parser.add_argument('available_holidays', type=int, default=25)
    parser.add_argument('department_id', type=str, help='you did not provide employee department id', required=True)

    return parser
