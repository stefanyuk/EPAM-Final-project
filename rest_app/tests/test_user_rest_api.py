import pytest
from flask import url_for
from rest_app.models import *
from rest_app.tests.data_for_unit_tests import test_user, credentials


def test_add_test_data_to_db():
    users = User.query.all()
    addresses = Address.query.all()
    employees = EmployeeInfo.query.all()
    departments = Department.query.all()

    assert len(users) == 11  # + admin user
    assert len(addresses) == 10
    assert len(employees) == 5
    assert len(departments) == 8
    assert departments[-1].name == 'Python'


def test_get_users_list(client):
    response = client.get(url_for('rp_api.user_list'), headers={'Authorization': f'Basic {credentials}'})
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 11
    assert data[0]['first_name'] == 'Charlton'
    assert data[-2]['username'] == 'sboadby9'


def test_get_users_list_without_auth(client):
    response = client.get(url_for('rp_api.user_list'))

    assert response.status_code == 401


def test_create_new_user(client):
    response = client.post(
        url_for('rp_api.user_list'),
        headers={'Authorization': f'Basic {credentials}'},
        json=test_user
    )

    data = response.get_json()
    users = User.query.all()

    assert response.status_code == 201
    assert 'user with id -' in data['message']
    assert users[-1].username == 'test_user'


@pytest.mark.parametrize(
    ('user_id', 'username'),
    (
            ('9da00efd-fe86-4b90-ac85-237c0eeaf7e6', 'cglyn0'),
            ('2c67e8e4-c499-4844-bc31-dd46f200bf00', 'ldally1'),
            ('6b6cefad-6d6e-4585-8f49-13bc468f3159', 'ehansford2')
    )
)
def test_get_user(client, user_id, username):
    response = client.get(
        url_for('rp_api.user', user_id=user_id),
        headers={'Authorization': f'Basic {credentials}'}
    )

    data = response.get_json()

    assert response.status_code == 200
    assert username in data['username']


@pytest.mark.parametrize(
    ('user_id', 'username'),
    (
            ('doesnotexist', 'nhealeas0'),
            ('doesnotexist2', 'jregler1'),
            ('doesnotexist3', 'gmcbeath2')
    )
)
def test_get_user_atypical_behaviour(client, user_id, username):
    response = client.get(
        url_for('rp_api.user', user_id=user_id),
        headers={'Authorization': f'Basic {credentials}'}
    )

    data = response.get_json()

    assert response.status_code == 404
    assert 'user with the provided id was not found' in data['message']


@pytest.mark.parametrize(
    ('user_id', 'new_username'),
    (
            ('9da00efd-fe86-4b90-ac85-237c0eeaf7e6', 'test1'),
            ('2c67e8e4-c499-4844-bc31-dd46f200bf00', 'test2'),
            ('6b6cefad-6d6e-4585-8f49-13bc468f3159', 'test3')
    )
)
def test_update_user(client, user_id, new_username):
    response = client.put(
        url_for('rp_api.user', user_id=user_id),
        headers={'Authorization': f'Basic {credentials}'},
        json={'username': new_username}
    )

    data = response.get_json()
    get_response = client.get(
        url_for('rp_api.user', user_id=user_id),
        headers={'Authorization': f'Basic {credentials}'}
    )

    get_data = get_response.get_json()

    assert response.status_code == 200
    assert 'has been updated' in data['message']
    assert new_username in get_data['username']


@pytest.mark.parametrize(
    ('user_id', 'new_username'),
    (
            ('test_id_1', 'test_1'),
            ('test_id_2', 'test_2'),
            ('test_id_3', 'test_3')
    )
)
def test_update_user_atypical_behaviour(client, user_id, new_username):
    response = client.put(
        url_for('rp_api.user', user_id=user_id),
        headers={'Authorization': f'Basic {credentials}'},
        json={'username': new_username}
    )

    data = response.get_json()

    assert response.status_code == 404
    assert 'user with the provided id was not found' in data['message']


@pytest.mark.parametrize('user_id', (
        'cc760630-afa5-4acd-ae68-a4d90ac9eeb3',
        '1a9ebbbe-a0ac-4081-a4a3-ae4624422757',
        'f7155f2b-2ad6-41c4-905c-f3ccfe77105b'
))
def test_delete_user(client, user_id):
    response = client.delete(
        url_for('rp_api.user', user_id=user_id),
        headers={'Authorization': f'Basic {credentials}'},
    )

    get_response = client.get(url_for('rp_api.user', user_id=user_id),
                              headers={'Authorization': f'Basic {credentials}'},
                              )

    get_data = get_response.get_json()

    assert response.status_code == 204
    assert get_response.status_code == 404
    assert 'user with the provided id was not found' in get_data['message']

