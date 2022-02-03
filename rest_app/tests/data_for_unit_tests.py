from base64 import b64encode

credentials = b64encode(b'admin:admin').decode('utf-8')

test_user = {
    'username': 'test_user',
    'password': 'passwordtest',
    'last_name': 'test_last',
    'email': 'testuser@gmail.com'
}

test_department = {
    'name': 'C++',
    'description': 'test department'
}

test_employee = {
    'salary': 3232.123,
    'available_holidays': 25,
    'first_name': 'Test',
    'last_name': 'TestSurname',
    'hire_date': '2022-02-03'
}

test_order = {
    'order_items': [
        {
            'product_id': 'Caffee Latte',
            'quantity': 2
        },
        {
            'product_id': 'Cafe au lait',
            'quantity': 3
        }
    ]
}


