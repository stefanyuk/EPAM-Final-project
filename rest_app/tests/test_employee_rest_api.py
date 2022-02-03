import pytest
from unittest.mock import patch
from flask import url_for
from rest_app.models import *
from rest_app.tests.data_for_unit_tests import test_employee


def test_get_employee_list_without_auth(client):
    response = client.get(url_for('employees.get_all'))

    assert response.status_code == 401


@patch('rest_app.models.user.User.verify_access_token')
def test_get_employees_list(mocked_verification, client, employee_data):
    mocked_verification.return_value = User.query.get('1')
    response = client.get(url_for('employees.get_all'), headers={f'Authorization': f'Bearer {"my-token"}'})

    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 4
    assert data[0]['first_name'] == 'Charlton'


@patch('rest_app.models.user.User.verify_access_token')
def test_create_new_employee(mocked_verification, client, create_tables, dept_data):
    mocked_verification.return_value = User.query.get('1')
    test_employee['department_id'] = dept_data[0].id

    response = client.post(
        url_for('employees.new'),
        headers={f'Authorization': f'Bearer {"my-token"}'},
        json=test_employee
    )

    data = response.get_json()

    assert response.status_code == 201
    assert test_employee['first_name'] in data['first_name']
    assert 'Java' == data['department']


@pytest.mark.parametrize(
    ('index', 'first_name'),
    (
        (0, 'Charlton'),
        (1, 'Liva'),
        (2, 'Emmalynn')
    )
)
@patch('rest_app.models.user.User.verify_access_token')
def test_get_employee(mocked_verification, client, index, first_name, employee_data):
    mocked_verification.return_value = User.query.get('1')
    response = client.get(
        url_for('employees.get', employee_id=employee_data[index].id),
        headers={f'Authorization': f'Bearer {"my-token"}'}
    )

    data = response.get_json()

    assert response.status_code == 200
    assert first_name in data['first_name']


@pytest.mark.parametrize(
    ('employee_id', 'first_name'),
    (
            ('doesnotexist', 'Test1'),
            ('doesnotexist2', 'Test2'),
            ('doesnotexist3', 'Test3')
    )
)
@patch('rest_app.models.user.User.verify_access_token')
def test_get_employee_atypical_behaviour(mocked_verification, client, create_tables, employee_id, first_name):
    mocked_verification.return_value = User.query.get('1')
    response = client.get(
        url_for('employees.get', employee_id=employee_id),
        headers={f'Authorization': f'Bearer {"my-token"}'}
    )

    assert response.status_code == 404


@pytest.mark.parametrize(
    ('index', 'new_name'),
    (
        (0, 'Charlton_test1'),
        (1, 'Liva_test2'),
        (2, 'Emmalynn_test3')
    )
)
@patch('rest_app.models.user.User.verify_access_token')
def test_update_employee(mocked_verification, client, index, new_name, employee_data, dept_data):
    mocked_verification.return_value = User.query.get('1')
    response = client.patch(
        url_for('employees.update', employee_id=employee_data[index].id),
        headers={f'Authorization': f'Bearer {"my-token"}'},
        json={'first_name': new_name, 'department_id': dept_data[3].id}
    )

    data = response.get_json()

    assert response.status_code == 200
    assert new_name in data['first_name']
    assert dept_data[3].name in data['department']


@pytest.mark.parametrize(
    ('employee_id', 'new_name'),
    (
            ('test_id_1', 'test_1'),
            ('test_id_2', 'test_2')
    )
)
@patch('rest_app.models.user.User.verify_access_token')
def test_update_employee_atypical_behaviour(mocked_verification, client, create_tables, employee_id, new_name):
    mocked_verification.return_value = User.query.get('1')
    response = client.patch(
        url_for('employees.update', employee_id=employee_id),
        headers={f'Authorization': f'Bearer {"my-token"}'},
        json={'first_name': new_name}
    )

    assert response.status_code == 404


@pytest.mark.parametrize('index', (0, 1, 2))
@patch('rest_app.models.user.User.verify_access_token')
def test_delete_employee(mocked_verification, client, index, employee_data):
    mocked_verification.return_value = User.query.get('1')
    response = client.delete(
        url_for('employees.delete', employee_id=employee_data[index].id),
        headers={f'Authorization': f'Bearer {"my-token"}'},
    )

    get_response = client.get(
        url_for('employees.get', employee_id=employee_data[index].id),
        headers={f'Authorization': f'Bearer {"my-token"}'},
    )

    assert response.status_code == 204
    assert get_response.status_code == 404


@pytest.mark.parametrize('index', (0, 1, 2))
@patch('rest_app.models.user.User.verify_access_token')
def test_if_employee_deletes_on_user_delete(mocked_verification, client, index, employee_data):
    mocked_verification.return_value = User.query.get('1')
    user_id = employee_data[index].user.id

    response = client.delete(
        url_for('users.delete', user_id=user_id),
        headers={f'Authorization': f'Bearer {"my-token"}'},
    )
    employee = EmployeeInfo.query.filter_by(user_id=user_id).first()

    assert response.status_code == 204
    assert employee is None
