from rest_app.models import Department, EmployeeInfo
from flask_restful import reqparse
from sqlalchemy import func, asc, desc
from uuid import uuid4
from rest_app import db
from rest_app.service.common_services import get_row_by_id, set_all_parser_args_to_unrequired


def add_department(name, description, dept_id=None):
    """
    Creates new department record in the database

    :param name: name of the new department
    :param description: description of the new department
    :param dept_id: department id
    """
    new_dept = Department(
        id=dept_id if dept_id else str(uuid4()),
        name=name,
        description=description
    )

    db.session.add(new_dept)
    db.session.commit()

    return new_dept


def department_data_to_dict(department):
    """
    Serializer that returns a dictionary from its fields

    :param department: department object that needs to be serialized
    :return: department information
    """
    avg_salary = get_average_dept_salary(department.id)
    total_employees = get_total_employees(department.id)

    department_info = {
        'id': department.id,
        'name': department.name,
        'average_department_salary': 0 if isinstance(avg_salary, int) else str(avg_salary.one()['avg_salary']),
        'total_employees': 0 if isinstance(total_employees, int) else str(total_employees.one()['qty']),
        'description': department.description
    }

    return department_info


def sort_dept_by_average_salary(sort_order='acs'):
    """
    Function that creates a query to get average salary for each department
    """
    order = asc if sort_order == 'asc' else desc

    query = db.session.query(Department)\
        .join(EmployeeInfo)\
        .group_by(Department.id)\
        .order_by(order(func.ROUND(func.AVG(EmployeeInfo.salary), 3)))

    return query


def sort_dept_by_total_employees(sort_order='asc'):
    """
    Creates a query to sort departments table by employees quantity
    """
    order = asc if sort_order == 'asc' else desc

    query = db.session.query(Department) \
        .join(EmployeeInfo)\
        .group_by(Department.id)\
        .order_by(order(func.COUNT(EmployeeInfo.department_id)))

    return query


def get_average_dept_salary(department_id):
    """
    Get average salary in the specific department

    :param department_id: unique id of the department
    """

    department = get_row_by_id(Department, department_id)

    if not department.employees.all():
        return 0

    query = db.session.query(Department.name, func.ROUND(func.AVG(EmployeeInfo.salary), 3).label('avg_salary'))\
        .outerjoin(EmployeeInfo)\
        .filter(Department.id == department_id)\
        .group_by(Department.name)

    return query


def get_total_employees(department_id):
    """
    Get total quantity of employees in the specific department

    :param department_id: unique id of the department
    """

    department = get_row_by_id(Department, department_id)

    if not department.employees.all():
        return 0

    query = db.session.query(Department.name, func.COUNT(EmployeeInfo.department_id).label('qty')) \
        .outerjoin(EmployeeInfo)\
        .filter(Department.id == department_id)\
        .group_by(Department.name)

    return query


def update_department_data(department_id, **kwargs):
    """
    Updates department's information in the database

    :param department_id: id of the department to be updated
    """
    department = get_row_by_id(Department, department_id)

    for key, value in kwargs.items():
        if value:
            setattr(department, key, value)

    db.session.commit()


def department_data_parser():
    """
    Creates a parser in order to parse information
    provided by user for department creation
    """

    parser = reqparse.RequestParser()

    parser.add_argument('name', type=str, help='you did not provide name of the department',
                        location=['json', 'form'], required=True)
    parser.add_argument('description', location=['json', 'form'], type=str)
    return parser


def department_form_data_parser():
    """
    Creates a parser in order to parse department information from the web form
    """
    parser = department_data_parser().copy()
    parser.replace_argument('name', location=['form'], required=False)

    return parser
