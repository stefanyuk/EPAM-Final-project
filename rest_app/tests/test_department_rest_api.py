import pytest
from flask import url_for
from rest_app.models import *
from rest_app.tests.data_for_unit_tests import test_department, credentials


def test_get_department_list_without_auth(client):
    response = client.get(url_for('rp_api.department_list'))

    assert response.status_code == 401


def test_get_departments_list(client, dept_data):
    response = client.get(url_for('rp_api.department_list'), headers={'Authorization': f'Basic {credentials}'})

    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 11
    assert data[-1]['name'] == 'Python'


def test_create_new_department(client):
    response = client.post(
        url_for('rp_api.department_list'),
        headers={'Authorization': f'Basic {credentials}'},
        json=test_department
    )

    data = response.get_json()
    departments = Department.query.all()

    assert response.status_code == 201
    assert 'department with id' in data['message']
    assert departments[-1].name == 'C++'


@pytest.mark.parametrize(
    ('index', 'name'),
    (
        (0, 'Java'),
        (1, 'Training'),
        (2, 'JavaScript')
    )
)
def test_get_department(client, index, name, dept_data):
    response = client.get(
        url_for('rp_api.department', department_id=dept_data[index].id),
        headers={'Authorization': f'Basic {credentials}'}
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
def test_get_department_atypical_behaviour(client, create_tables, department_id, name):
    response = client.get(
        url_for('rp_api.department', department_id=department_id),
        headers={'Authorization': f'Basic {credentials}'}
    )

    data = response.get_json()

    assert response.status_code == 404
    assert 'department with the provided id was not found' in data['message']



@pytest.mark.parametrize(
    ('index', 'new_name'),
    (
        (0, 'Java_test1'),
        (1, 'Training_test2'),
        (2, 'JavaScript_test3')
    )
)
def test_update_department(client, index, new_name, dept_data):
    response = client.put(
        url_for('rp_api.department', department_id=dept_data[index].id),
        headers={'Authorization': f'Basic {credentials}'},
        json={'name': new_name}
    )

    data = response.get_json()

    get_response = client.get(
        url_for('rp_api.department', department_id=dept_data[index].id),
        headers={'Authorization': f'Basic {credentials}'}
    )

    get_data = get_response.get_json()

    assert response.status_code == 200
    assert get_response.status_code == 200
    assert 'has been updated' in data['message']
    assert new_name in get_data['name']


@pytest.mark.parametrize(
    ('department_id', 'new_name'),
    (
            ('test_id_1', 'test_1'),
            ('test_id_2', 'test_2')
    )
)
def test_update_department_atypical_behaviour(client, create_tables, department_id, new_name):
    response = client.put(
        url_for('rp_api.department', department_id=department_id),
        headers={'Authorization': f'Basic {credentials}'},
        json={'name': new_name}
    )

    data = response.get_json()

    assert response.status_code == 404
    assert 'department with the provided id was not found' in data['message']


@pytest.mark.parametrize('index', (0, 1, 2))
def test_delete_department(client, index, dept_data):
    response = client.delete(
        url_for('rp_api.department', department_id=dept_data[index].id),
        headers={'Authorization': f'Basic {credentials}'},
    )

    get_response = client.get(
        url_for('rp_api.department', department_id=dept_data[index].id),
        headers={'Authorization': f'Basic {credentials}'},
    )

    get_data = get_response.get_json()

    assert response.status_code == 204
    assert get_response.status_code == 404
    assert 'department with the provided id was not found' in get_data['message']


