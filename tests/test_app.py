import pytest
from app import app, users_list, products_list


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    yield client


def test_main_route(client):
    response = client.get('/main')
    assert response.status_code == 200


def test_users_route(client):
    response = client.get('/users')
    assert response.status_code == 200


def test_add_user_route(client):
    initial_users_count = len(users_list)
    response = client.post('/add_user', data={'user_name': 'TestUser'})
    assert response.status_code == 302  # Check for redirect
    assert len(users_list) == initial_users_count + 1


def test_products_route(client):
    response = client.get('/products')
    assert response.status_code == 200


def test_get_products_by_category_route(client):
    response = client.get('/get_products_by_category?get_category=Електроніка')
    assert response.status_code == 200
    assert b"\xD0\x95\xD0\xBB\xD0\xB5\xD0\xBA\xD1\x82\xD1\x80\xD0\xBE\xD0\xBD\xD1\x96\xD0\xBA\xD0\xB0" in response.data


def test_add_product_route(client):
    initial_products_count = len(products_list['Електроніка'])
    response = client.post('/add_product',
                           data={'category': 'Електроніка', 'product_name': 'TestProduct', 'product_price': 100})
    assert response.status_code == 302  # Check for redirect
    assert len(products_list['Електроніка']) == initial_products_count + 1


def test_cart_route(client):
    response = client.get('/cart')
    assert response.status_code == 200
