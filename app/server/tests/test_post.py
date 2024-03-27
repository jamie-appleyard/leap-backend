from fastapi.testclient import TestClient
from app.server.app import app

client = TestClient(app)

#GET
##get posts
def test_get_posts():
    response = client.get('/post')
    assert response.status_code == 200
    expected_data = [[]]
    expected_response = {
	"data": expected_data,
	"code": 200,
	"message": "Post data retrieved successfully"
    }
    assert response.json()['message'] == "Post data retrieved successfully"

# def test_get_posts():
#     response = client.get('/not-an-endpoint')
#     assert response.status_code == 404
#     expected_response = {
# 	  "code": 404,
# 	  "message": "Not found"
#     }
#     assert response.json() == expected_response

##get posts by id
def test_get_post_by_id():
    response = client.get('/post/6604260b5f82618899662b78') 
    assert response.status_code == 200
    expected_data = [{
            "id": "6604260b5f82618899662b78",
            "topic_id": "660426095f82618899662b14",
            "title": "Nulla mollis molestie lorem. Quisque ut erat. Curabitur gravida nisi at nibh. In hac habitasse platea dictumst. Aliquam augue quam, sollicitudin vitae, consectetuer eget, rutrum at, lorem.",
            "user_id": "660426095f82618899662ab0",
            "votes": 68,
            "post_image": "http://dummyimage.com/107x100.png/ff4444/ffffff",
            "type": "post"
    }
    ]
    expected_response = {
    "data": expected_data,
    "code": 200,
    "message": "Post data retrieved successfully"
    }
    assert response.json() == expected_response

##post doesn't exist
def test_get_post_by_id():
    response = client.get('/post/fjbsk54feios2n') 
    assert response.status_code == 404
    expected_response = {
    "error": 'An error occurred',
    "code": 404,
    "message": "Post doesn't exist"
    }
    assert response.json() == expected_response

#POST
##post a post
def test_post_post():
    post_data = {
            'topic_id': '660424791268a3b4266679e2',
            'post_body': 'This is a new post!',
            'title': 'My Title',
            'user_id': '660424791268a3b42666797e',
            'votes': 0,
            'post_image': 'https://my-image.jpeg',
            'type': [],
    }

    response = client.post('/post', json=post_data) 
    assert response.status_code == 201
    expected_response = {
    "data":   {
            '_id': '6604247b1268a3b426667aa9',  #replace with id
            'topic_id': '660424791268a3b4266679e2',
            'post_body': 'This is a new post!',
            'title': 'My Title',
            'user_id': '660424791268a3b42666797e',
            'votes': 0,
            'post_image': 'https://my-image.jpeg',
            'type': [],
    }
,
    "code": 201,
    "message": "Post added successfully"
    }
    assert response.json() == expected_response

##post an incomplete object
def test_post_post():
    post_data = {
            'topic_id': '78ewsdahucijonhcu',
            'post_body': 'This is a new post!',
            'user_id': '7dshudjakbfahy',
            'votes': 0,
            'post_image': 'https://my-image.jpeg',
            'type': [],
    }
    response = client.post('/post', json=post_data) 
    assert response.status_code == 400
    expected_response = {
    "code": 400,
    "message": "Post does not meet requirements"
    }
    assert response.json() == expected_response

#DELETE
##post deleted succesfully
def test_del_post():
    response = client.delete('/post/6604247b1268a3b426667aa9') 
    assert response.status_code == 204
    assert response.json()['message'] == "Post deleted successfully"

##post doesn't exist
def test_del_post():
    response = client.delete('/post/fnkdgnksjdnfa9') 
    assert response.status_code == 404
    assert response.json()['error'] == 'An error occurred'

#PUT
##post updated successsfully
def test_put_post():
    put_data = {
            'post_body': 'This is a new post!',
            'title': 'My Title',
            'post_image': 'https://my-image.jpeg',
            'type': [],
    }

    response = client.put('/post', json=put_data) 
    assert response.status_code == 200
    assert response.json()['message'] == 'Post updated successfully'


