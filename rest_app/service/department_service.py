from rest_app.models import Department, EmployeeInfo
from flask_restful import reqparse
from sqlalchemy import func, asc, desc
from uuid import uuid4
from rest_app import db


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
