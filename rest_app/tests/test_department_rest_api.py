import pytest
from flask import url_for
from unittest.mock import patch
from rest_app.models import *
from rest_app.tests.data_for_unit_tests import test_department


def test_get_department_list_without_auth(client):
    response = client.get(url_for('departments.get_all'))

    assert response.status_code == 401


@patch('rest_app.models.user.User.verify_access_token')
def test_get_departments_list(mocked_verification, client, dept_data):
    mocked_verification.return_value = User.query.get('1')
    response = client.get(url_for('departments.get_all'), headers={f'Authorization': f'Bearer {"my-token"}'})

    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 11
    assert data[-1]['name'] == 'Python'


@patch('rest_app.models.user.User.verify_access_token')
def test_create_new_department(mocked_verification, client):
    mocked_verification.return_value = User.query.get('1')
    response = client.post(
        url_for('departments.new'),
        headers={f'Authorization': f'Bearer {"my-token"}'},
        json=test_department
    )

    data = response.get_json()

    assert response.status_code == 201
    assert test_department['name'] in data['name']


@pytest.mark.parametrize(
    ('index', 'name'),
    (
        (0, 'Java'),
        (1, 'Training'),
        (2, 'JavaScript')
    )
)
@patch('rest_app.models.user.User.verify_access_token')
def test_get_department(mocked_verification, client, index, name, dept_data):
    mocked_verification.return_value = User.query.get('1')
    response = client.get(
        url_for('departments.get', department_id=dept_data[index].id),
        headers={f'Authorization': f'Bearer {"my-token"}'}
    )

    data = response.get_json()

    assert response.status_code == 200
    assert name in data['name']


@pytest.mark.parametrize(
    ('department_id', 'name'),
    (
            ('doesnotexist', 'Test1'),
            ('doesnotexist2', 'Test2'),
            ('doesnotexist3', 'Test3')
    )
)
@patch('rest_app.models.user.User.verify_access_token')
def test_get_department_atypical_behaviour(mocked_verification, client, create_tables, department_id, name):
    mocked_verification.return_value = User.query.get('1')
    response = client.get(
        url_for('departments.get', department_id=department_id),
        headers={f'Authorization': f'Bearer {"my-token"}'}
    )

    assert response.status_code == 404


@pytest.mark.parametrize(
    ('index', 'new_name'),
    (
        (0, 'Java_test1'),
        (1, 'Training_test2'),
        (2, 'JavaScript_test3')
    )
)
@patch('rest_app.models.user.User.verify_access_token')
def test_update_department(mocked_verification, client, index, new_name, dept_data):
    mocked_verification.return_value = User.query.get('1')
    response = client.patch(
        url_for('departments.update', department_id=dept_data[index].id),
        headers={f'Authorization': f'Bearer {"my-token"}'},
        json={'name': new_name}
    )

    data = response.get_json()

    assert response.status_code == 200
    assert new_name in data['name']


@pytest.mark.parametrize(
    ('department_id', 'new_name'),
    (
            ('test_id_1', 'test_1'),
            ('test_id_2', 'test_2')
    )
)
@patch('rest_app.models.user.User.verify_access_token')
def test_update_department_atypical_behaviour(mocked_verification, client, create_tables, department_id, new_name):
    mocked_verification.return_value = User.query.get('1')
    response = client.patch(
        url_for('departments.update', department_id=department_id),
        headers={f'Authorization': f'Bearer {"my-token"}'},
        json={'name': new_name}
    )

    assert response.status_code == 404


@pytest.mark.parametrize('index', (0, 1, 2))
@patch('rest_app.models.user.User.verify_access_token')
def test_delete_department(mocked_verification, client, index, dept_data):
    mocked_verification.return_value = User.query.get('1')
    response = client.delete(
        url_for('departments.delete', department_id=dept_data[index].id),
        headers={f'Authorization': f'Bearer {"my-token"}'},
    )

    assert response.status_code == 204


@pytest.mark.parametrize('index', (0, 1, 2))
@patch('rest_app.models.user.User.verify_access_token')
def test_employee_set_null_on_dept_delete(mocked_verification, client, index, dept_data):
    mocked_verification.return_value = User.query.get('1')
    employees = Department.query.get(dept_data[index].id).employees

    response = client.delete(
        url_for('departments.delete', department_id=dept_data[index].id),
        headers={f'Authorization': f'Bearer {"my-token"}'},
    )

    for employee in employees:
        assert employee.department is None

    assert response.status_code == 204