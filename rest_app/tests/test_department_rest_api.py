import pytest
from flask import url_for
from rest_app.models import *
from rest_app.tests.data_for_unit_tests import test_department, credentials


def test_get_departments_list(client):
    response = client.get(url_for('rp_api.department_list'), headers={'Authorization': f'Basic {credentials}'})

    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 5
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
    assert departments[-1].name == 'JavaScript'



@pytest.mark.parametrize(
    ('department_id', 'name'),
    (
            ('1749490a-e61e-45d3-b341-14703af555ec', 'Java'),
            ('7a4440bf-f8e6-4620-8eb0-795dfefeeff6', 'Training'),
            ('09568e78-221c-4b58-9851-f3ddd799e465', 'Python')
    )
)
def test_get_department(client, department_id, name):
    response = client.get(
        url_for('rp_api.department', department_id=department_id),
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
def test_get_department_atypical_behaviour(client, department_id, name):
    response = client.get(
        url_for('rp_api.department', department_id=department_id),
        headers={'Authorization': f'Basic {credentials}'}
    )

    data = response.get_json()

    assert response.status_code == 404
    assert 'department with the provided id was not found' in data['message']



@pytest.mark.parametrize(
    ('department_id', 'new_name'),
    (
            ('1749490a-e61e-45d3-b341-14703af555ec', 'Java_test'),
            ('7a4440bf-f8e6-4620-8eb0-795dfefeeff6', 'Training_test'),
            ('09568e78-221c-4b58-9851-f3ddd799e465', 'Python_test')
    )
)
def test_update_department(client, department_id, new_name):
    response = client.put(
        url_for('rp_api.department', department_id=department_id),
        headers={'Authorization': f'Basic {credentials}'},
        json={'name': new_name}
    )

    data = response.get_json()

    get_response = client.get(
        url_for('rp_api.department', department_id=department_id),
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
def test_update_department_atypical_behaviour(client, department_id, new_name):
    response = client.put(
        url_for('rp_api.department', department_id=department_id),
        headers={'Authorization': f'Basic {credentials}'},
        json={'name': new_name}
    )

    data = response.get_json()

    assert response.status_code == 404
    assert 'department with the provided id was not found' in data['message']
