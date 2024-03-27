from fastapi.testclient import TestClient
from app.server.app import app
from seed_test_db import seed_test_data
import asyncio

client = TestClient(app)

def print_log(log):
    print('\n', log)

@seed_test_data
def test_get_users():
    response = client.get('/user')
    assert response.status_code == 200
    assert len(response.json()['data'][0]) == 100
    for key in response.json()['data'][0][0].keys():
        assert key in ['id', 'username', 'email']
    assert response.json()['message'] == "User data retrieved successfully"

def test_users_404():
    response = client.get('/userrs')
    print_log(response)
    assert response.status_code == 404