import datetime as dt
import random
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
    departments = [Department.create(**department) for department in departments]

    return departments


def create_categories(categories):
    categories_data = {}

    for category in categories:
        c = Category.create(name=category)
        categories_data[c.name] = c.id

    return categories_data


def main(max_qty):
    test_info = create_test_info()
    users = test_info['users']
    departments = create_departments(test_info['departments'])
    categories = create_categories(['Bakery', 'Coffee', 'Tea'])
    products = []

    for product in test_info['products']:
        category_id = categories[product.pop('category')]
        prod = Product.create(category_id=category_id, **product)
        products.append({'product_id': prod.id, 'quantity': random.choice(range(1, 4))})

    orders = (order for order in test_info['orders'])
    addresses = (address for address in test_info['addresses'])
    employees = (employee for employee in test_info['employees'])

    for i in range(max_qty):
        user = User.create(**users[i])
        address = Address.create(user_id=user.id, **next(addresses))
        if user.is_employee:
            department_id = random.choice(departments).id
            EmployeeInfo.create(
                user_id=user.id, department_id=department_id, **next(employees)
            )

        r = random.choice(range(1, 4))
        order = next(orders)
        Order.create(
            {
                'order_items': [random.choice(products) for i in range(r)],
                'user_id': user.id,
                'address_id': address.id,
                'comments': order['comments'],
                'order_date': order['order_date'],
                'order_time': dt.datetime.strftime(dt.datetime.utcnow(), '%H:%M:%S')
            }
        )


if __name__ == '__main__':
    main(30)
