import importlib
import re
import sys

import pytest

PASSWORD = 'test-student-password'


def csrf_token(client, path='/'):
    page = client.get(path).get_data(as_text=True)
    return re.search(r'name="csrf_token" value="([^"]+)"', page).group(1)


def login(client, name='Alice Johansson', password=PASSWORD):
    return client.post('/login', data={
        'username': name, 'password': password, 'csrf_token': csrf_token(client),
    })


@pytest.fixture
def server(tmp_path, monkeypatch):
    monkeypatch.setenv('SECRET_KEY', 'test-only-session-secret')
    monkeypatch.setenv('DATABASE_PATH', str(tmp_path / 'lunch.db'))
    monkeypatch.setenv('SESSION_COOKIE_SECURE', 'false')
    sys.modules.pop('web_interface.flask_server', None)
    module = importlib.import_module('web_interface.flask_server')
    module.app.config['TESTING'] = True
    student_id = module.db.add_student({'name': 'Alice Johansson'})
    module.db.set_student_password(student_id, PASSWORD)
    module.db.add_meal({'name': 'Pasta', 'price': 50})
    yield module
    module.db.db.close()
    sys.modules.pop('web_interface.flask_server', None)


def test_login_and_logout(server):
    client = server.app.test_client()
    response = login(client, name='  alice johansson  ')
    assert response.status_code == 302
    assert response.headers['Location'].endswith('/dashboard')
    assert 'HttpOnly' in response.headers['Set-Cookie']
    assert 'SameSite=Lax' in response.headers['Set-Cookie']
    with client.session_transaction() as state:
        assert state['student_id'] == 1
        assert state['username'] == 'Alice Johansson'
        assert state['auth_version'] == 2
    assert client.get('/logout').status_code == 405
    client.post('/logout', data={'csrf_token': csrf_token(client, '/dashboard')})
    assert client.get('/api/meals').status_code == 401


@pytest.mark.parametrize('name,password', [
    ('', PASSWORD), ('Unknown Student', PASSWORD), ('Alice Johansson', 'wrong'),
    ('Alice Johansson', ''),
])
def test_invalid_login(server, name, password):
    client = server.app.test_client()
    assert login(client, name, password).status_code == 302
    with client.session_transaction() as state:
        assert 'student_id' not in state


@pytest.mark.parametrize('method,path', [
    ('get', '/api/meals'), ('post', '/api/order'), ('post', '/api/rate'),
    ('post', '/api/import-openfoodfacts'),
])
def test_api_requires_login(server, method, path):
    client = server.app.test_client()
    token = csrf_token(client)
    assert getattr(client, method)(path, headers={'X-CSRFToken': token}).status_code == 401


def test_orders_and_ratings(server):
    client = server.app.test_client()
    login(client)
    token = csrf_token(client, '/dashboard')
    headers = {'X-CSRFToken': token}
    assert client.get('/api/meals').get_json()[0]['name'] == 'Pasta'
    assert client.post('/api/order', json={'meal_id': 1}, headers=headers).status_code == 200
    orders = server.db.get_student_transactions(1)
    assert len(orders) == 1
    assert orders[0]['meal_id'] == 1
    assert client.post('/api/rate', json={'meal_id': 1, 'rating': 4}, headers=headers).status_code == 200
    assert client.get('/api/meals').get_json()[0]['rating'] == 4
    assert client.post('/api/rate', json={'meal_id': 1, 'rating': 6}, headers=headers).status_code == 400


def test_login_error_does_not_expose_database_details(server, monkeypatch):
    def unavailable(*args, **kwargs):
        raise RuntimeError('private-database-path')
    monkeypatch.setattr(server.db, 'authenticate_student', unavailable)
    client = server.app.test_client()
    response = client.post('/login', data={
        'username': 'Alice Johansson', 'password': PASSWORD, 'csrf_token': csrf_token(client),
    }, follow_redirects=True)
    assert b'private-database-path' not in response.data
    assert b'Login is temporarily unavailable' in response.data


def test_secret_is_required(tmp_path, monkeypatch):
    monkeypatch.delenv('SECRET_KEY', raising=False)
    monkeypatch.setenv('DATABASE_PATH', str(tmp_path / 'lunch.db'))
    sys.modules.pop('web_interface.flask_server', None)
    with pytest.raises(RuntimeError, match='Set SECRET_KEY'):
        importlib.import_module('web_interface.flask_server')


def test_missing_csrf_rejects_login(server):
    response = server.app.test_client().post('/login', data={
        'username': 'Alice Johansson', 'password': PASSWORD,
    })
    assert response.status_code == 400


@pytest.mark.parametrize('path', ['/api/order', '/api/rate', '/logout'])
def test_missing_csrf_rejects_authenticated_requests(server, path):
    client = server.app.test_client()
    login(client)
    assert client.post(path, json={'meal_id': 1, 'rating': 4}).status_code == 400
    assert len(server.db.get_student_transactions(1)) == 0
    with client.session_transaction() as state:
        assert state['student_id'] == 1


def test_csrf_from_another_session_is_rejected(server):
    first, second = server.app.test_client(), server.app.test_client()
    token = csrf_token(first)
    csrf_token(second)
    assert second.post('/login', data={
        'username': 'Alice Johansson', 'password': PASSWORD, 'csrf_token': token,
    }).status_code == 400


def test_old_name_only_session_is_rejected(server):
    client = server.app.test_client()
    with client.session_transaction() as state:
        state['username'] = 'Alice Johansson'
        state['student_id'] = 1
    assert client.get('/api/meals').status_code == 401


def test_password_hash_and_reset(server):
    stored = server.db.db.execute('SELECT password_hash FROM student_credentials')[0][0]
    assert stored != PASSWORD
    assert PASSWORD not in stored
    server.db.set_student_password(1, 'a-new-student-password')
    assert server.db.authenticate_student('Alice Johansson', PASSWORD) is None
    assert server.db.authenticate_student('Alice Johansson', 'a-new-student-password') is not None


def test_existing_student_needs_password(server):
    student_id = server.db.add_student({'name': 'Existing Student'})
    assert server.db.authenticate_student('Existing Student', PASSWORD) is None
    server.db.set_student_password(student_id, PASSWORD)
    assert server.db.authenticate_student('Existing Student', PASSWORD)['id'] == student_id


def test_duplicate_student_names_are_rejected(server):
    student_id = server.db.add_student({'name': 'alice johansson'})
    server.db.set_student_password(student_id, PASSWORD)
    assert server.db.authenticate_student('Alice Johansson', PASSWORD) is None


def test_credentials_migration_preserves_existing_data(tmp_path):
    import sqlite3
    from lunch_system_database import SchoolLunchDB
    database = tmp_path / 'existing.db'
    with sqlite3.connect(database) as connection:
        connection.execute('CREATE TABLE students (id INTEGER PRIMARY KEY, name TEXT NOT NULL)')
        connection.execute('INSERT INTO students VALUES (7, "Existing Student")')
    db = SchoolLunchDB(str(database))
    try:
        assert db.db.execute('SELECT id FROM students')[0]['id'] == 7
        db.set_student_password(7, PASSWORD)
        assert db.authenticate_student('Existing Student', PASSWORD)['id'] == 7
    finally:
        db.db.close()
