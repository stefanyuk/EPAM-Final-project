import pytest
import random
from rest_app import create_app, db
from rest_app.database import create_superuser
from config import TestingConfig
from rest_app.populate_db_with_data import main, create_departments, create_test_info, \
    add_user, add_employee, add_address, create_order, create_categories, add_product

test_info = create_test_info()

@pytest.fixture()
def app(postgresql):
    TestingConfig.SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{postgresql.info.user}:@{postgresql.info.host}' + \
                                            f':{postgresql.info.port}/{postgresql.info.dbname}'
    app = create_app(test_config=TestingConfig)

    return app


@pytest.fixture(autouse=True)
def create_tables(app):
    with app.app_context():
        db.create_all()

    create_superuser()


@pytest.fixture
def dept_data(users_data):
    departments = create_departments(test_info['departments'])

    return departments


@pytest.fixture
def users_data():
    addresses = test_info['addresses']
    users = test_info['users']
    new_users = []
    for i in range(4):
        user = add_user(**users[i])
        new_users.append(user)
        add_address(user_id=user.id, **addresses[i])

    return new_users


@pytest.fixture
def employee_data(users_data, dept_data):
    employees = (employee for employee in test_info['employees'])
    employee_info = []

    for i in range(4):
        employee = add_employee(
            is_employee=None, user_id=users_data[i].id, department_id=dept_data[i].id, first_name=None,
            last_name=None, birth_date=None, is_admin=None, email=None,
            password=None, phone_number=None, **next(employees)
        )

        employee_info.append(employee)

    return employee_info


@pytest.fixture
def products():
    categories = create_categories(['Bakery', 'Coffee', 'Tea'])
    new_products = []

    for index, product in enumerate(test_info['products']):
        category_id = categories[product['category']]
        product_info = {k: v for k, v in product.items() if k != 'category'}
        prod = add_product(**product_info, category_id=category_id)
        new_products.append({'id': prod.id, 'quantity': random.choice(range(1, 4))})
        if index == 4:
            break

    return new_products

@pytest.fixture
def order_data(users_data, products):
    orders = (order for order in test_info['orders'])
    new_orders = []

    for user in users_data:
        r = random.choice(range(1, 4))
        new_orders.append(
            create_order(
                [random.choice(products) for i in range(r)],
                user_id=user.id,
                address_id=user.addresses.first().id,
                main_key='id',
                **next(orders)
            )
        )

    return new_orders


@pytest.fixture
def add_data_to_db():
    main(10)
