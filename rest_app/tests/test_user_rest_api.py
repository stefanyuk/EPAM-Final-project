import pytest
from flask import url_for
from rest_app.models import *
from rest_app.tests.data_for_unit_tests import test_user, credentials


def test_get_users_list(client, users_data):
    response = client.get(url_for('rp_api.user_list'), headers={'Authorization': f'Basic {credentials}'})
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 5
    assert data[1]['first_name'] == 'Charlton'
    assert data[-1]['username'] == 'ehanshawe3'


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
    ('index', 'username'),
    (
        (0, 'cglyn0'),
        (1, 'ldally1'),
        (2, 'ehansford2')
    )
)
def test_get_user(client, index, username, users_data):
    response = client.get(
        url_for('rp_api.user', user_id=users_data[index].id),
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
def test_get_user_atypical_behaviour(client, create_tables, user_id, username):
    response = client.get(
        url_for('rp_api.user', user_id=user_id),
        headers={'Authorization': f'Basic {credentials}'}
    )

    data = response.get_json()

    assert response.status_code == 404
    assert 'user with the provided id was not found' in data['message']


@pytest.mark.parametrize(
    ('index', 'new_username'),
    (
        (0, 'cglyn0_new'),
        (1, 'ldally1_new2'),
        (2, 'ehansford2_new3')
    )
)
def test_update_user(client, index, new_username, users_data):
    response = client.patch(
        url_for('rp_api.user', user_id=users_data[index].id),
        headers={'Authorization': f'Basic {credentials}'},
        json={'username': new_username}
    )

    data = response.get_json()
    get_response = client.get(
        url_for('rp_api.user', user_id=users_data[index].id),
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
def test_update_user_atypical_behaviour(client, users_data, user_id, new_username):
    response = client.patch(
        url_for('rp_api.user', user_id=user_id),
        headers={'Authorization': f'Basic {credentials}'},
        json={'username': new_username}
    )

    data = response.get_json()

    assert response.status_code == 404
    assert 'user with the provided id was not found' in data['message']


@pytest.mark.parametrize('index', (0, 1, 2))
def test_delete_user(client, index, users_data):
    response = client.delete(
        url_for('rp_api.user', user_id=users_data[index].id),
        headers={'Authorization': f'Basic {credentials}'},
    )

    get_response = client.get(
        url_for('rp_api.user', user_id=users_data[index].id),
        headers={'Authorization': f'Basic {credentials}'},
    )

    get_data = get_response.get_json()

    assert response.status_code == 204
    assert get_response.status_code == 404
    assert 'user with the provided id was not found' in get_data['message']

