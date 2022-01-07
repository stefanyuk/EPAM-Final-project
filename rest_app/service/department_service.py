from rest_app.models import Department, EmployeeInfo
from flask_restful import reqparse
from sqlalchemy import func
from uuid import uuid4
from rest_app import db
from rest_app.service.common_services import get_row_by_id


def add_department(name, description):
    """
    Creates new department record in the database

    :param name: name of the new department
    :param description: description of the new department
    """
    new_dept = Department(id=str(uuid4()), name=name, description=description)

    db.session.add(new_dept)
    db.session.commit()

    return new_dept.id


def department_data_to_dict(department):
    """
    Serializer that returns a dictionary from its fields

    :param department: department object that needs to be serialized
    :return: department information
    """
    department_info = {
        'id': department.id,
        'name': department.name,
        'average_department_salary': float(get_average_dept_salary(department.id)),
        'total_employees': get_total_employees(department.id),
        'description': department.description
    }

    return department_info


def get_average_dept_salary(department_id):
    """
    Get average salary in the specific department

    :param department_id: unique id of the department
    """

    department = get_row_by_id(Department, department_id)

    if not department.employees.all():
        return 0

    query = db.session.query(Department.name, func.ROUND(func.AVG(EmployeeInfo.salary), 3).label('avg_salary')) \
        .join(EmployeeInfo) \
        .filter(Department.id == department_id) \
        .group_by(Department.name).one()

    return query['avg_salary']


def get_total_employees(department_id):
    """
    Get total quantity of employees in the specific department

    :param department_id: unique id of the department
    """

    department = get_row_by_id(Department, department_id)

    if not department.employees.all():
        return 0

    query = db.session.query(Department.name, func.COUNT(EmployeeInfo.department_id).label('qty')) \
        .join(EmployeeInfo) \
        .filter(Department.id == department_id) \
        .group_by(Department.name).one()

    return query['qty']


def update_department(department_id, **kwargs):
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

    parser.add_argument('name', type=str, help='name of the department')
    parser.add_argument('description', type=str, help='description of the department')

    return parser
