from rest_app.models import EmployeeInfo, Department


def get_all_employees_by_department(department_name):
    """
    Creates a query that searches for all employees who belong to the provided department

    :param department_name: name of the department
    """
    dept = Department.query.filter_by(name=department_name).first()
    query = EmployeeInfo.query.filter_by(department_id=dept.id)

    return query
