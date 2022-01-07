from base64 import b64encode

credentials = b64encode(b'admin:admin').decode('utf-8')

test_user = {
    'username': 'test_user',
    'password_hash': 'test',
    'last_name': 'test_last'
}

test_department = {
    'name': 'JavaScript',
    'description': 'test department'
}


