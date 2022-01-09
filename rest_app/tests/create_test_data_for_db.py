import datetime
import json
import random
from rest_app.models import *
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('postgresql+psycopg2://test:test@localhost:5432/restwebapp')
session = sessionmaker(engine)()

basedir = os.path.abspath(os.path.dirname(__file__))

test_info = {}


def create_test_info():
    for file in next(os.walk(os.path.join(basedir, 'db_schemas')))[2]:
        with open(os.path.join(basedir, 'db_schemas', file)) as f:
            name = file[:file.find('.json')]
            test_info[name] = json.load(f)


def create_departments(ses, departments):
    for dept in departments:
        department = Department(**dept)
        ses.add(department)

    ses.commit()


def create_user(ses, user_info):
    user = User(**user_info)

    ses.add(user)
    ses.commit()

    return user


def create_employee(ses, user_id, department_id, **kwargs):
    employee = EmployeeInfo(
        **kwargs,
        user_id=user_id,
        department_id=department_id
    )

    ses.add(employee)
    ses.commit()


def create_address(ses, user_id, **kwargs):
    address = Address(
        user_id=user_id,
        **kwargs
    )

    ses.add(address)
    ses.commit()


def create_order(ses, user_id, **kwargs):
    order = Order(
        order_date=datetime.datetime.now().date(),
        user_id=user_id,
        order_time=datetime.datetime.now().time()
    )

    ses.add(address)
    ses.commit()


def main(ses):
    create_test_info()
    users = test_info['user']
    departments = test_info['department']
    employees = (employee for employee in test_info['employee'])
    addresses = (address for address in test_info['address'])

    create_departments(ses, departments)

    for user in users:
        user = create_user(ses, user)
        if user.is_employee:
            department_id = random.choice(test_info['department'])['id']
            create_employee(ses, user.id, department_id, **next(employees))
            create_address(ses, user.id, **next(addresses))


if __name__ == '__main__':
    main(session)
