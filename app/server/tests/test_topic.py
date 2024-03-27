from fastapi.testclient import TestClient
from app.server.app  import app

client = TestClient(app)

#HAPPY PATH TESTS
def test_get_topics():
    expected_data = [
        [
        {
            "id": "6602fb87487854aa68abf3f8",
            "topic_name": "stonemasonry",
            "summary": "cutting rocks"
        },
        {
            "id": "6602fb9b487854aa68abf3f9",
            "topic_name": "stonemasonry",
            "summary": "cutting rocks"
        },
        {
            "id": "6602fbcb487854aa68abf3fa",
            "topic_name": "stonemasonry",
            "summary": "cutting rocks"
        },
        {
            "id": "6602fd4a7a300e8fa602ef97",
            "topic_name": "stonemasonry",
            "summary": "cutting rocks"
        },
        {
            "id": "6602fd5d7a300e8fa602ef98",
            "topic_name": "stonemasonry",
            "summary": "cutting rocks"
        },
        {
            "id": "6602fd7d7a300e8fa602ef99",
            "topic_name": "stonemasonry",
            "summary": "cutting rocks"
        },
        {
            "id": "660300cd36e524bc057733e7",
            "topic_name": "stonemasonry",
            "summary": "cutting rocks"
        },
        {
            "id": "6603ed6f5033ce0f84c7d6b0",
            "topic_name": "stuff",
            "summary": "thangs"
        },
        {
            "id": "6603ed8c5033ce0f84c7d6b1",
            "topic_name": "nuthin",
            "summary": "zilch"
        },
        {
            "id": "6603edaf5033ce0f84c7d6b2",
            "topic_name": "test",
            "summary": "testing testing this thing on?"
        }
        ]
    ]
    expected_response = {
        "data": expected_data,
        "code": 200,
        "message": "Topics data retrieved successfully"
    }
    response = client.get('/topic')
    assert response.status_code == 200
    assert response.json() == expected_response

def test_get_topics_by_id():
    test_id = "test id here!"
    expcted_data = [
        {
        "id": "6603edaf5033ce0f84c7d6b2",
        "topic_name": "test",
        "summary": "testing testing this thing on?"
        }
    ]
    expected_response = {
        "data": expcted_data,
        "code": 200,
        "message": "Topic data retrieved successfully"
    }
    response = client.get(f'/topic/{test_id}')
    assert response.status_code == 200
    assert response.json() == expected_response

def test_post_topic():
    expected_name = "primb grimbus"
    expected_summary = "the frungiest grum"
    expected_code = 200
    expected_message = "Topic added successfully"
    response = client.post("/topic", 
        json={
            "topic_name": "primb grimbus",
            "summary": "the frungiest grum"
            })
    assert response.status_code == 200
    assert response.json().data.topic_name == expected_name
    assert response.json().data.summary == expected_summary
    assert response.json().code == expected_code
    assert response.json().message == expected_message

def test_put_topic():
    test_id = "test id here!"

    expected_response = {
        "data": [
            f"topic with ID: {test_id} update successful"
        ],
        "code": 200,
        "message": "Topic updated Successfully"
    }
    response = client.put(f"/topic/{test_id}", 
        json={
            "topic_name": "shwaomp friendly"
            ,"summary": "criminal"
            })
    assert response.status_code == 200
    assert response.json() == expected_response

def test_delete_topic():
    test_id = "test id here!"
    expected_response = {
        "data": [
            f"topic with ID: {test_id} removed"
            ],
        "code": 200,
        "message": "topic deleted successfully"
    }
    response = client.put(f"/topic/{test_id}")
    assert response.status_code == 200
    assert response.json() == expected_response


#ERROR TESTING
def test_error_get_topic_by_id():
    test_id = "bad test id here!"
    response = client.get(f'/topic/{test_id}')
    assert response == {
        "error":"An error occurred.",
        "code": 404,
        "message": "topic does not exist"
        }

def test_error_post_topic_bad_types():
    test_data = {
        "topic_name": 23,
        "summary": 32
    }
    response = client.post("/topic", json=test_data)
    assert response == {
        "detail": [
            {
            "type": "string_type",
            "loc": [
                "body",
                "topic_name"
            ],
            "msg": "Input should be a valid string",
            "input": 23,
            "url": "https://errors.pydantic.dev/2.6/v/string_type"
            },
            {
            "type": "string_type",
            "loc": [
                "body",
                "summary"
            ],
            "msg": "Input should be a valid string",
            "input": 32,
            "url": "https://errors.pydantic.dev/2.6/v/string_type"
            }
        ]
    }

def test_error_put_topic_bad_id():
    test_data = {
            "topic_name": "primb grimbus",
            "summary": "the frungiest grum"
            }
    test_id = "bad test id here!"
    response = client.post(f"/topic/{test_id}", json=test_data)
    assert response == {
        "error": "An error occurred",
        "code": 404,
        "message": "error topic does not exist"
    }

def test_error_put_topic_types():
    test_id = "test id here!"
    test_data = {
            "topic_name": 1,
            "summary": 2
            }
    response = client.post(f"/topic/{test_id}", json=test_data)
    assert response == {
        "detail": [
            {
            "type": "string_type",
            "loc": [
                "body",
                "topic_name"
            ],
            "msg": "Input should be a valid string",
            "input": 1,
            "url": "https://errors.pydantic.dev/2.6/v/string_type"
            },
            {
            "type": "string_type",
            "loc": [
                "body",
                "summary"
            ],
            "msg": "Input should be a valid string",
            "input": 2,
            "url": "https://errors.pydantic.dev/2.6/v/string_type"
            }
        ]
    }

def test_error_delete_topic():
    test_id = "bad test id here!"
    response = client.delete(f"/topic/{test_id}")
    assert response == {
        "error": "An error occcurred",
        "code": 404,
        "message": "topic with id {test_id} does not exist"
    }


    
    