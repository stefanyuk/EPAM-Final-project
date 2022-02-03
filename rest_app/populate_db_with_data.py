import random
from rest_app.service.department_service import add_department
from rest_app.service.employee_service import add_employee
from rest_app.service.address_service import add_address
from rest_app.service.order_service import create_order
from rest_app.service.product_service import add_product
from rest_app.service.category_service import add_category
from rest_app.models import *
import os
import json

basedir = os.path.abspath(os.path.dirname(__file__))


def create_test_info():
    test_info = {}

    for file in next(os.walk(os.path.join(basedir, 'tests', 'db_schemas')))[2]:
        with open(os.path.join(basedir, 'tests', 'db_schemas', file)) as f:
            name = file[:file.find('.json')]
            test_info[name] = json.load(f)

    return test_info


def create_departments(departments):
    departments = [add_department(**department) for department in departments]

    return departments


def create_categories(categories):
    categories_data = {}

    for category in categories:
        c = add_category(category)
        categories_data[c.name] = c.id

    return categories_data


def main(max_qty):
    test_info = create_test_info()
    users = test_info['users']
    departments = create_departments(test_info['departments'])
    categories = create_categories(['Bakery', 'Coffee', 'Tea'])
    products = []

    for product in test_info['products']:
        category_id = categories[product['category']]
        product.pop('category')
        prod = add_product(**product, category_id=category_id)
        products.append({'id': prod.id, 'quantity': random.choice(range(1, 4))})

    orders = (order for order in test_info['orders'])
    addresses = (address for address in test_info['addresses'])
    employees = (employee for employee in test_info['employees'])

    for i in range(max_qty):
        user = User.create(**users[i])
        address = add_address(user_id=user.id, **next(addresses))
        if user.is_employee:
            department_id = random.choice(departments).id
            add_employee(
                is_employee=None, user_id=user.id, department_id=department_id, first_name=None,
                last_name=None, birth_date=None, is_admin=None, email=None,
                password=None, phone_number=None, **next(employees)
            )

        r = random.choice(range(1, 4))
        create_order(
            [random.choice(products) for i in range(r)],
            user_id=user.id,
            address_id=address.id,
            **next(orders),
            main_key='id'
        )


if __name__ == '__main__':
    main(251)
