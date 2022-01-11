import random
from rest_app.service.department_service import add_department
from rest_app.service.employee_service import add_employee
from rest_app.service.address_service import add_address
from rest_app.service.order_service import create_order
from rest_app.service.product_service import add_product
from rest_app.service.user_service import add_user
from rest_app.service.category_service import add_category
import os
import json

basedir = os.path.abspath(os.path.dirname(__file__))

test_info = {}


def create_test_info():
    for file in next(os.walk(os.path.join(basedir, 'tests', 'db_schemas')))[2]:
        with open(os.path.join(basedir, 'tests', 'db_schemas', file)) as f:
            name = file[:file.find('.json')]
            test_info[name] = json.load(f)


def create_departments(departments):
    departments = [add_department(**department) for department in departments]

    return departments


def create_categories(categories):
    categories = [add_category(category) for category in categories]

    return categories


def main(max_qty):
    create_test_info()
    users = test_info['users']
    departments = create_departments(test_info['departments'])
    categories = create_categories(['Bakery', 'Coffee', 'Croissant', 'Tea'])
    products = []

    for product in test_info['products']:
        category_id = random.choice(categories).id
        prod = add_product(**product, category_id=category_id)
        products.append(prod)

    orders = (order for order in test_info['orders'])
    addresses = (address for address in test_info['addresses'])
    employees = (employee for employee in test_info['employees'])

    for i in range(max_qty):
        user = add_user(**users[i])
        address = add_address(user_id=user.id, **next(addresses))
        if user.is_employee:
            department_id = random.choice(departments).id
            add_employee(user_id=user.id, department_id=department_id, **next(employees))

        create_order(
            [random.choice(products).title for i in range(3)],
            user_id=user.id,
            address_id=address.id,
            **next(orders)
        )


if __name__ == '__main__':
    main(251)
