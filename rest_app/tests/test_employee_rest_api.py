import pytest
from unittest.mock import patch
from flask import url_for
from rest_app.models import *
from rest_app.tests.data_for_unit_tests import credentials, test_employee


def test_get_employee_list_without_auth(client):
    response = client.get(url_for('rp_api.employee_list'))

    assert response.status_code == 401


@patch('rest_app.models.user.User.verify_access_token')
def test_get_employees_list(mocked_verification, client, employee_data):
    mocked_verification.return_value = User.query.get('1')
    response = client.get(url_for('rp_api.employee_list'), headers={'Authorization': f'Basic {credentials}'})

    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 4
    assert data[0]['first_name'] == 'Charlton'


def test_create_new_employee(client, create_tables, dept_data):
    test_employee['department_id'] = dept_data[0].id

    response = client.post(
        url_for('rp_api.employee_list'),
        headers={'Authorization': f'Basic {credentials}'},
        json=test_employee
    )

    data = response.get_json()
    employees = EmployeeInfo.query.all()

    assert response.status_code == 201
    assert 'employee with id -' in data['message']
    assert len(employees) == 1
    assert employees[-1].department_id == dept_data[0].id


@pytest.mark.parametrize(
    ('index', 'first_name'),
    (
        (0, 'Charlton'),
        (1, 'Liva'),
        (2, 'Emmalynn')
    )
)
def test_get_employee(client, index, first_name, employee_data):
    response = client.get(
        url_for('rp_api.employee', employee_id=employee_data[index].id),
        headers={'Authorization': f'Basic {credentials}'}
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
def test_get_employee_atypical_behaviour(client, create_tables, employee_id, first_name):
    response = client.get(
        url_for('rp_api.employee', employee_id=employee_id),
        headers={'Authorization': f'Basic {credentials}'}
    )

    data = response.get_json()

    assert response.status_code == 404
    assert 'employee with the provided id was not found' in data['message']


@pytest.mark.parametrize(
    ('index', 'new_name'),
    (
        (0, 'Charlton_test1'),
        (1, 'Liva_test2'),
        (2, 'Emmalynn_test3')
    )
)
def test_update_employee(client, index, new_name, employee_data):
    response = client.patch(
        url_for('rp_api.employee', employee_id=employee_data[index].id),
        headers={'Authorization': f'Basic {credentials}'},
        json={'first_name': new_name}
    )

    data = response.get_json()

    get_response = client.get(
        url_for('rp_api.employee', employee_id=employee_data[index].id),
        headers={'Authorization': f'Basic {credentials}'}
    )

    get_data = get_response.get_json()

    assert response.status_code == 200
    assert get_response.status_code == 200
    assert 'has been updated' in data['message']
    assert new_name in get_data['first_name']


@pytest.mark.parametrize(
    ('employee_id', 'new_name'),
    (
            ('test_id_1', 'test_1'),
            ('test_id_2', 'test_2')
    )
)
def test_update_employee_atypical_behaviour(client, create_tables, employee_id, new_name):
    response = client.patch(
        url_for('rp_api.employee', employee_id=employee_id),
        headers={'Authorization': f'Basic {credentials}'},
        json={'name': new_name}
    )

    data = response.get_json()

    assert response.status_code == 404
    assert 'employee with the provided id was not found' in data['message']


@pytest.mark.parametrize('index', (0, 1, 2))
def test_delete_employee(client, index, employee_data):
    response = client.delete(
        url_for('rp_api.employee', employee_id=employee_data[index].id),
        headers={'Authorization': f'Basic {credentials}'},
    )

    get_response = client.get(
        url_for('rp_api.employee', employee_id=employee_data[index].id),
        headers={'Authorization': f'Basic {credentials}'},
    )

    get_data = get_response.get_json()

    assert response.status_code == 204
    assert get_response.status_code == 404
    assert 'employee with the provided id was not found' in get_data['message']
