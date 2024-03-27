from fastapi.testclient import TestClient
from app.server.app import app

client = TestClient(app)

def test_get_users():
    response = client.get('/user')
    assert response.status_code == 200
    expected_data = [
		[
			{
				"id": "6601a0d85dd24d8180a84804",
				"username": "speedy-gonzales",
				"email": "None@none.com"
			},
			{
				"id": "6601a1080ccebfaf15c91265",
				"username": "speedy-gonzales",
				"email": "jamie@jamie.com"
			}
		]
	]
    expected_response = {
	"data": expected_data,
	"code": 200,
	"message": "User data retrieved successfully"
    }
    assert response.json() == expected_response