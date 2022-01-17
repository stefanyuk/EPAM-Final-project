from rest_app.models import *


def test_add_test_data_to_db(add_data_to_db):
    users = User.query.all()
    addresses = Address.query.all()
    employees = EmployeeInfo.query.all()
    departments = Department.query.all()

    assert len(users) == 11  # + admin user
    assert len(addresses) == 10
    assert len(employees) == 5
    assert len(departments) == 11
    assert departments[-1].name == 'Python'

