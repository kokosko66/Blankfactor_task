import pytest
from app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_login(client):
    response = client.post('/login', json={'username': 'user', 'password': 'password'})
    assert response.status_code == 200
    assert 'access_token' in response.get_json()

def test_compute_endpoint(client):
    response = client.post('/login', json={'username': 'user', 'password': 'password'})
    access_token = response.get_json()['access_token']

    data = {
        'user': 'test_user',
        'name': 'test_request',
        'file': (open('test.csv', 'rb'), 'test.csv')
    }
    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.post('/api/compute', headers=headers, data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert 'total' in response.get_json()
