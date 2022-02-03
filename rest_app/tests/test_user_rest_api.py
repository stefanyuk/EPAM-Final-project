import pytest
from unittest.mock import patch
from flask import url_for
from rest_app.models import *
from rest_app.tests.data_for_unit_tests import test_user


@patch('rest_app.models.user.User.verify_access_token')
def test_get_users_list(mocked_verification, client, users_data):
    mocked_verification.return_value = User.query.get('1')
    response = client.get(url_for('users.get_all'), headers={f'Authorization': f'Bearer {"my-token"}'})
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 5
    assert data[1]['first_name'] == 'Charlton'
    assert data[-1]['username'] == 'ehanshawe3'


def test_get_users_list_without_auth(client):
    response = client.get(url_for('users.get', user_id=1))

    assert response.status_code == 401


@patch('rest_app.models.user.User.verify_access_token')
def test_create_new_user(mocked_verification, client):
    mocked_verification.return_value = User.query.get('1')
    response = client.post(
        url_for('users.new'),
        headers={f'Authorization': f'Bearer {"my-token"}'},
        json=test_user
    )

    data = response.get_json()

    assert response.status_code == 201
    assert test_user['username'] in data['username']
    assert test_user['email'] == data['email']


@pytest.mark.parametrize(
    ('index', 'username'),
    (
        (0, 'cglyn0'),
        (1, 'ldally1'),
        (2, 'ehansford2')
    )
)
@patch('rest_app.models.user.User.verify_access_token')
def test_get_user(mocked_verification, client, index, username, users_data):
    mocked_verification.return_value = User.query.get('1')
    response = client.get(
        url_for('users.get', user_id=users_data[index].id),
        headers={f'Authorization': f'Bearer {"my-token"}'}
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
@patch('rest_app.models.user.User.verify_access_token')
def test_get_user_atypical_behaviour(mocked_verification, client, create_tables, user_id, username):
    mocked_verification.return_value = User.query.get('1')
    response = client.get(
        url_for('users.get', user_id=user_id),
        headers={f'Authorization': f'Bearer {"my-token"}'}
    )

    assert response.status_code == 404


@pytest.mark.parametrize(
    ('index', 'new_username'),
    (
        (0, 'cglyn0_new'),
        (1, 'ldally1_new2'),
        (2, 'ehansford2_new3')
    )
)
@patch('rest_app.models.user.User.verify_access_token')
def test_update_user(mocked_verification, client, index, new_username, users_data):
    mocked_verification.return_value = User.query.get('1')
    response = client.patch(
        url_for('users.update', user_id=users_data[index].id),
        headers={f'Authorization': f'Bearer {"my-token"}'},
        json={'username': new_username}
    )

    data = response.get_json()

    assert response.status_code == 200
    assert new_username in data['username']


@pytest.mark.parametrize(
    ('user_id', 'new_username'),
    (
            ('test_id_1', 'test_1'),
            ('test_id_2', 'test_2'),
            ('test_id_3', 'test_3')
    )
)
@patch('rest_app.models.user.User.verify_access_token')
def test_update_user_atypical_behaviour(mocked_verification, client, users_data, user_id, new_username):
    mocked_verification.return_value = User.query.get('1')
    response = client.patch(
        url_for('users.update', user_id=user_id),
        headers={f'Authorization': f'Bearer {"my-token"}'},
        json={'username': new_username}
    )

    assert response.status_code == 404


@pytest.mark.parametrize('index', (0, 1, 2))
@patch('rest_app.models.user.User.verify_access_token')
def test_delete_user(mocked_verification, client, index, users_data):
    mocked_verification.return_value = User.query.get('1')
    response = client.delete(
        url_for('users.delete', user_id=users_data[index].id),
        headers={f'Authorization': f'Bearer {"my-token"}'},
    )

    get_response = client.get(
        url_for('users.get', user_id=users_data[index].id),
        headers={f'Authorization': f'Bearer {"my-token"}'},
    )

    assert response.status_code == 204
    assert get_response.status_code == 404


