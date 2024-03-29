from fastapi.testclient import TestClient
from app.server.app import app
from seed_test_db import seed_test_data
import asyncio

client = TestClient(app)

def print_log(log):
    print('\n', log)

def test_get_users():
    response = client.get('/user')
    assert response.status_code == 200
    assert isinstance(response.json()["data"], list)
    assert len(response.json()["data"][0]) == 100
    assert response.json()["message"] == "User data retrieved successfully"
    for key in response.json()['data'][0][0].keys():
        assert key in ['id', 'username', 'email']
    
def test_get_user_by_id():
    user_id = "66040d2344d383be9bd03053"
    response = client.get(f'/user/{user_id}')
    assert response.status_code == 200
    assert isinstance(response.json()["data"], str)
    assert response.json()["message"] == "User data retrieved successfully"
    
def test_get_invalid_user_by_id():
    response = client.get('/user/invalid_user_id')
    assert response.status_code == 422
    assert "detail" in response.json()
    
def test_add_user_data():
    new_user = {
        "username": "new_user",
        "email": "new_user@example.com"
    }
    response = client.post('/user', json=new_user)
    assert response.status_code == 200
    assert isinstance(response.json()["data"], str)
    assert response.json()["message"] == "User added successfully"
    
def test_add_invalid_user_data():
    invalid_user = {
        "username": "",
        "email": "invalid_email"
    }
    response = client.post('/user', json=invalid_user)
    assert response.status_code == 422
    assert "detail" in response.json()
    
def test_delete_user_data():
    new_user = {
        "username": "delete_me",
        "email": "delete_me@example.com"
    }
    response = client.post('/user', json=new_user)
    user_id = response.json()["data"]["id"]
    delete_response = client.delete(f'/user/{user_id}')
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "User deleted successfully"
    get_response = client.get(f'/user/{user_id}')
    assert get_response.status_code == 404
    
def test_delete_invalid_user_data():
    response = client.delete('/user/invalid_user_id')
    assert response.status_code == 422
    assert "detail" in response.json()

def test_update_user_data():
    new_user = {
        "username": "update_me",
        "email": "update_me@example.com"
    }
    response = client.post('/user', json=new_user)
    user_id = response.json()["data"]["id"]
    updated_user_data = {
        "email": "updated_email@example.com"
    }
    update_response = client.put(f'/user/{user_id}', json=updated_user_data)
    assert update_response.status_code == 200
    assert isinstance(update_response.json()["data"], str)
    assert update_response.json()["message"] == "User updated successfully"
    get_response = client.get(f'/user/{user_id}')
    assert get_response.status_code == 200
    assert get_response.json()["data"]["email"] == "updated_email@example.com"

def test_update_invalid_user_data():
    invalid_user_data = {
        "email": "invalid_email"
    }
    response = client.put('/user/invalid_user_id', json=invalid_user_data)
    assert response.status_code == 422
    assert "detail" in response.json()
    

def test_users_404():
    response = client.get('/userrs')
    print_log(response)
    assert response.status_code == 404
