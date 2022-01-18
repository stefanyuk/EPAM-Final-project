import pytest
from flask import url_for
from rest_app.models import *
from rest_app.tests.data_for_unit_tests import credentials, test_order


def test_create_new_order_without_user_id(client, users_data, order_data):
    response = client.post(
        url_for('rp_api.order_list'),
        headers={'Authorization': f'Basic {credentials}'},
        json=test_order
    )

    data = response.get_json()

    assert response.status_code == 400
    assert {'user_id': 'you did not provide user id'} == data['message']


def test_create_new_order_without_address_id(client, users_data, order_data):
    test_order['user_id'] = users_data[0].id

    response = client.post(
        url_for('rp_api.order_list'),
        headers={'Authorization': f'Basic {credentials}'},
        json=test_order
    )

    data = response.get_json()

    assert response.status_code == 400
    assert {'address_id': 'you did not provide address id'} == data['message']


def test_get_orders_list_without_auth(client):
    response = client.get(url_for('rp_api.order_list'))

    assert response.status_code == 401


def test_get_orders_list(client, order_data):
    response = client.get(url_for('rp_api.order_list'), headers={'Authorization': f'Basic {credentials}'})

    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 4


def test_create_new_order(client, users_data, order_data):
    test_order['address_id'] = users_data[0].addresses.first().id
    test_order['user_id'] = users_data[0].id

    response = client.post(
        url_for('rp_api.order_list', main_key='title'),
        headers={'Authorization': f'Basic {credentials}'},
        json=test_order
    )

    data = response.get_json()
    orders = Order.query.all()

    assert response.status_code == 201
    assert 'order with id -' in data['message']
    assert orders[-1].user_id == test_order['user_id']


def test_create_new_order_without_query_string(client, users_data, order_data):
    test_order['address_id'] = users_data[0].addresses.first().id
    test_order['user_id'] = users_data[0].id

    response = client.post(
        url_for('rp_api.order_list'),
        headers={'Authorization': f'Basic {credentials}'},
        json=test_order
    )

    data = response.get_json()

    assert response.status_code == 400
    assert 'please provide key by which products should be searched' in data['message']


@pytest.mark.parametrize('index', (0, 1, 2))
def test_get_order(client, index, order_data):
    response = client.get(
        url_for('rp_api.order', order_id=order_data[index].id),
        headers={'Authorization': f'Basic {credentials}'}
    )

    assert response.status_code == 200


@pytest.mark.parametrize('order_id', ('doesnotexist', 'doesnotexist2', 'doesnotexist3'))
def test_get_order_atypical_behaviour(client, create_tables, order_id):
    response = client.get(
        url_for('rp_api.order', order_id=order_id),
        headers={'Authorization': f'Basic {credentials}'}
    )

    data = response.get_json()

    assert response.status_code == 404
    assert 'order with the provided id was not found' in data['message']


@pytest.mark.parametrize(
    ('index', 'new_status'),
    (
            (0, 'delivered'),
            (1, 'ready for deliver'),
            (2, 'test_update')
    )
)
def test_update_order(client, index, new_status, order_data):
    response = client.put(
        url_for('rp_api.order', order_id=order_data[index].id, main_key='title'),
        headers={'Authorization': f'Basic {credentials}'},
        json={'status': new_status}
    )

    data = response.get_json()
    get_response = client.get(
        url_for('rp_api.order', order_id=order_data[index].id),
        headers={'Authorization': f'Basic {credentials}'}
    )

    get_data = get_response.get_json()

    assert response.status_code == 200
    assert 'has been updated' in data['message']
    assert new_status in get_data['status']


@pytest.mark.parametrize(
    ('order_id', 'new_status'),
    (
            ('test_id_1', 'test_1'),
            ('test_id_2', 'test_2')
    )
)
def test_update_order_atypical_behaviour(client, create_tables, order_id, new_status):
    response = client.put(
        url_for('rp_api.order', order_id=order_id, main_key='title'),
        headers={'Authorization': f'Basic {credentials}'},
        json={'status': new_status}
    )

    data = response.get_json()

    assert response.status_code == 404
    assert 'order with the provided id was not found' in data['message']


@pytest.mark.parametrize('index', (0, 1, 2))
def test_delete_order(client, index, order_data):
    response = client.delete(
        url_for('rp_api.order', order_id=order_data[index].id),
        headers={'Authorization': f'Basic {credentials}'},
    )

    get_response = client.get(
        url_for('rp_api.order', order_id=order_data[index].id),
        headers={'Authorization': f'Basic {credentials}'},
    )

    get_data = get_response.get_json()

    assert response.status_code == 204
    assert get_response.status_code == 404
    assert 'order with the provided id was not found' in get_data['message']
