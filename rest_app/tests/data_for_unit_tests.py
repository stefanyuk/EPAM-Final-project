from base64 import b64encode

credentials = b64encode(b'admin:admin').decode('utf-8')

test_user = {
    'username': 'test_user',
    'password_hash': 'test',
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
    'birth_date': '1990-10-22',
    'city': 'New York',
    'street': 'TEST',
    'street_number': 23,
    'postal_code': '91-048'
}

test_order = {
    'products': [
        {
            'title': 'Caffee Latte',
            'quantity': 2
        },
        {
            'title': 'Cafe au lait',
            'quantity': 3
        }
    ]
}


