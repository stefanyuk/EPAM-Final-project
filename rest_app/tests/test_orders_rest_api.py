import pytest
from unittest.mock import patch
from flask import url_for
from rest_app.models import *
from rest_app.tests.data_for_unit_tests import credentials, test_order


@patch('rest_app.models.user.User.verify_access_token')
def test_create_new_order_without_user_id(mocked_verification, client, users_data, order_data):
    mocked_verification.return_value = User.query.get('1')
    response = client.post(
        url_for('orders_api.new'),
        headers={f'Authorization': f'Bearer {"my-token"}'},
        json=test_order
    )
    data = response.get_json()

    assert "Missing data for required field." in data['messages']['json']['user_id']
    assert "Missing data for required field." in data['messages']['json']['address_id']
    assert response.status_code == 400


@patch('rest_app.models.user.User.verify_access_token')
def test_create_new_order_without_address_id(mocked_verification, client, users_data, order_data):
    mocked_verification.return_value = User.query.get('1')
    test_order['user_id'] = users_data[0].id

    response = client.post(
        url_for('orders_api.new'),
        headers={f'Authorization': f'Bearer {"my-token"}'},
        json=test_order
    )

    data = response.get_json()

    assert response.status_code == 400
    assert "Missing data for required field." in data['messages']['json']['address_id']


def test_get_orders_list_without_auth(client):
    response = client.get(url_for('orders_api.get_all'))

    assert response.status_code == 401


@patch('rest_app.models.user.User.verify_access_token')
def test_get_orders_list(mocked_verification, client, order_data):
    mocked_verification.return_value = User.query.get('1')
    response = client.get(url_for('orders_api.get_all'), headers={f'Authorization': f'Bearer {"my-token"}'})

    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 4


@patch('rest_app.models.user.User.verify_access_token')
def test_create_new_order(mocked_verification, client, users_data, products):
    mocked_verification.return_value = User.query.get('1')
    test_order['address_id'] = users_data[0].addresses.first().id
    test_order['user_id'] = users_data[0].id
    test_order['order_items'][0]['product_id'] = products[0]['product_id']
    test_order['order_items'][1]['product_id'] = products[1]['product_id']

    response = client.post(
        url_for('orders_api.new'),
        headers={f'Authorization': f'Bearer {"my-token"}'},
        json=test_order
    )

    data = response.get_json()

    assert response.status_code == 201
    assert 'id' in data
    assert data['user'] == users_data[0].username


@pytest.mark.parametrize('index', (0, 1, 2))
@patch('rest_app.models.user.User.verify_access_token')
def test_get_order(mocked_verification, client, index, order_data):
    mocked_verification.return_value = User.query.get('1')
    response = client.get(
        url_for('orders_api.get', order_id=order_data[index].id),
        headers={f'Authorization': f'Bearer {"my-token"}'}
    )

    assert response.status_code == 200


@pytest.mark.parametrize('order_id', ('doesnotexist', 'doesnotexist2', 'doesnotexist3'))
@patch('rest_app.models.user.User.verify_access_token')
def test_get_order_atypical_behaviour(mocked_verification, client, create_tables, order_id):
    mocked_verification.return_value = User.query.get('1')
    response = client.get(
        url_for('orders_api.get', order_id=order_id),
        headers={f'Authorization': f'Bearer {"my-token"}'}
    )

    assert response.status_code == 404


@pytest.mark.parametrize(
    ('index', 'new_status'),
    (
            (0, 'delivered'),
            (1, 'ready for deliver'),
            (2, 'test_update')
    )
)
@patch('rest_app.models.user.User.verify_access_token')
def test_update_order(mocked_verification, client, index, new_status, order_data):
    mocked_verification.return_value = User.query.get('1')
    response = client.patch(
        url_for('orders_api.get', order_id=order_data[index].id),
        headers={f'Authorization': f'Bearer {"my-token"}'},
        json={'status': new_status}
    )

    data = response.get_json()

    assert response.status_code == 200
    assert new_status in data['status']


@pytest.mark.parametrize(
    ('order_id', 'new_status'),
    (
            ('test_id_1', 'test_1'),
            ('test_id_2', 'test_2')
    )
)
@patch('rest_app.models.user.User.verify_access_token')
def test_update_order_atypical_behaviour(mocked_verification, client, create_tables, order_id, new_status):
    mocked_verification.return_value = User.query.get('1')
    response = client.patch(
        url_for('orders_api.get', order_id=order_id),
        headers={f'Authorization': f'Bearer {"my-token"}'},
        json={'status': new_status}
    )

    assert response.status_code == 404


@pytest.mark.parametrize('index', (0, 1, 2))
@patch('rest_app.models.user.User.verify_access_token')
def test_delete_order(mocked_verification, client, index, order_data):
    mocked_verification.return_value = User.query.get('1')
    response = client.delete(
        url_for('orders_api.delete', order_id=order_data[index].id),
        headers={f'Authorization': f'Bearer {"my-token"}'},
    )

    get_response = client.get(
        url_for('orders_api.get', order_id=order_data[index].id),
        headers={f'Authorization': f'Bearer {"my-token"}'},
    )

    items = OrderItem.query.filter_by(order_id=order_data[index].id).all()

    assert response.status_code == 204
    assert get_response.status_code == 404
    assert len(items) == 0
