import pytest
import sys
import os
from flask import render_template

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, users_list, products_list, place_order, make_order


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


def test_place_order(client):
    with app.test_request_context('/place_order', method='POST', data={'selected_items': ['item1_10', 'item2_20']}):
        response = place_order()
        expected_html = render_template('cart.html',
                                        selected_products=[{'name': 'item1', 'price': 10},
                                                           {'name': 'item2', 'price': 20}],
                                        total_price=30)
        assert response.data == expected_html.encode('utf-8')


def test_make_order(client):
    with app.test_request_context('/make_order', method='POST'):
        response = make_order()
        assert response.status_code == 302
