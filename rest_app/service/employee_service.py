from rest_app.models import EmployeeInfo
from rest_app.service.user_service import add_user, user_data_parser
from rest_app.service.address_service import add_address
from rest_app.service.common_services import get_row_by_id
import datetime
from uuid import uuid4
from rest_app import db


def add_employee(username, first_name, last_name, gender, salary, phone_number, department_id,
                 city, postal_code, street, street_number, hire_date, birth_date, is_admin, is_employee,
                 email, password):
    """
    Add new employee to the database

    :param username: employee username
    :param first_name: employee name
    :param last_name: employee surname
    :param email: employee email
    :param password: password to login to the system
    :param gender: employee gender
    :param salary: employee salary
    :param phone_number: employee phone number
    :param hire_date: date when employee was hired
    :param birth_date: date when employee was born
    :param is_admin: database attribute that specifies user rights
    :param is_employee: database attribute that defines whether a user is employee
    :param department_id: id of the department where employee works
    :param city: city where employee is located
    :param postal_code: country postal code
    :param street: name of the street
    :param street_number: number of the street
    """
    user_id = add_user(username, password, first_name, last_name, email, phone_number, gender,
                       birth_date, is_admin, is_employee)

    add_address(user_id, city, postal_code, street, street_number)

    employee = EmployeeInfo(
        id=str(uuid4()),
        hire_date=hire_date,
        department_id=department_id,
        salary=salary,
        user_id=user_id,
    )

    db.session.add(employee)
    db.session.commit()

    return employee.id


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

    :param employee_id: unique employee identificator
    """
    employee = get_row_by_id(EmployeeInfo, employee_id)
    user = employee.user

    user_fields = {k: kwargs[k] for k in list(kwargs)[:10]}
    employee_data_fields = {k: kwargs[k] for k in list(kwargs)[15:]}

    for field in user_fields:
        if kwargs[field]:
            setattr(user, field, kwargs[field])

    for field in employee_data_fields:
        if kwargs[field]:
            setattr(employee, field, kwargs[field])

    db.session.commit()


def employee_data_parser():
    """
    Creates a parser in order to parse information
    provided by user for employee creation
    """
    user_parser_copy = user_data_parser().copy()

    user_parser_copy.add_argument('city', type=str, help='city name')
    user_parser_copy.add_argument('street', type=str, help='name of the street')
    user_parser_copy.add_argument('street_number', type=str, help='number of the street')
    user_parser_copy.add_argument('postal_code', type=str, help='postal code of the city where employee lives')
    user_parser_copy.add_argument('hire_date', type=str, help='date when employee was hired',
                                  default=datetime.datetime.now().date())
    user_parser_copy.add_argument('salary', type=float, help='salary of the employee')
    user_parser_copy.add_argument('available_holidays', type=int, help='holidays that employee can use')
    user_parser_copy.add_argument('department_id', type=str, help='department of the employee')

    return user_parser_copy
