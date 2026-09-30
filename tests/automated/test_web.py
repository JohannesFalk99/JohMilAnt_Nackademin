import importlib
import sys

import pytest


@pytest.fixture
def server(tmp_path, monkeypatch):
    monkeypatch.setenv('SECRET_KEY', 'test-only-session-secret')
    monkeypatch.setenv('DATABASE_PATH', str(tmp_path / 'lunch.db'))
    monkeypatch.setenv('SESSION_COOKIE_SECURE', 'false')
    sys.modules.pop('web_interface.flask_server', None)
    module = importlib.import_module('web_interface.flask_server')
    module.app.config['TESTING'] = True
    module.db.add_student({'name': 'Alice Johansson'})
    module.db.add_meal({'name': 'Pasta', 'price': 50})
    yield module
    module.db.db.close()
    sys.modules.pop('web_interface.flask_server', None)


def test_login_and_logout(server):
    client = server.app.test_client()
    assert client.get('/').status_code == 200
    response = client.post('/login', data={'username': '  alice johansson  '})
    assert response.status_code == 302
    assert response.headers['Location'].endswith('/dashboard')
    assert 'HttpOnly' in response.headers['Set-Cookie']
    assert 'SameSite=Lax' in response.headers['Set-Cookie']
    with client.session_transaction() as state:
        assert state['student_id'] == 1
        assert state['username'] == 'Alice Johansson'
    assert client.get('/dashboard').status_code == 200
    client.get('/logout')
    assert client.get('/api/meals').status_code == 401


@pytest.mark.parametrize('name', ['', 'Unknown Student'])
def test_invalid_login(server, name):
    client = server.app.test_client()
    assert client.post('/login', data={'username': name}).status_code == 302
    with client.session_transaction() as state:
        assert 'student_id' not in state


@pytest.mark.parametrize('method,path', [
    ('get', '/api/meals'),
    ('post', '/api/order'),
    ('post', '/api/rate'),
    ('post', '/api/import-openfoodfacts'),
])
def test_api_requires_login(server, method, path):
    assert getattr(server.app.test_client(), method)(path).status_code == 401


def test_orders_and_ratings(server):
    client = server.app.test_client()
    client.post('/login', data={'username': 'Alice Johansson'})
    meals = client.get('/api/meals').get_json()
    assert meals[0]['name'] == 'Pasta'
    assert client.post('/api/order', json={'meal_id': 1}).status_code == 200
    orders = server.db.get_student_transactions(1)
    assert len(orders) == 1
    assert orders[0]['meal_id'] == 1
    assert client.post('/api/rate', json={'meal_id': 1, 'rating': 4}).status_code == 200
    assert client.get('/api/meals').get_json()[0]['rating'] == 4
    assert client.post('/api/rate', json={'meal_id': 1, 'rating': 6}).status_code == 400


def test_login_error_does_not_expose_database_details(server, monkeypatch):
    import sqlite3
    def unavailable(*args, **kwargs):
        raise sqlite3.OperationalError('private-database-path')
    monkeypatch.setattr(sqlite3, 'connect', unavailable)
    response = server.app.test_client().post(
        '/login', data={'username': 'Alice Johansson'}, follow_redirects=True)
    assert b'private-database-path' not in response.data
    assert b'Login is temporarily unavailable' in response.data


def test_secret_is_required(tmp_path, monkeypatch):
    monkeypatch.delenv('SECRET_KEY', raising=False)
    monkeypatch.setenv('DATABASE_PATH', str(tmp_path / 'lunch.db'))
    sys.modules.pop('web_interface.flask_server', None)
    with pytest.raises(RuntimeError, match='Set SECRET_KEY'):
        importlib.import_module('web_interface.flask_server')
