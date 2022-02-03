from rest_app.models import Department, EmployeeInfo
from sqlalchemy import func, asc, desc
from rest_app import db


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
