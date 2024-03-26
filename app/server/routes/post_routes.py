from fastapi import APIRouter, Body

#Translate python dictionaries in to JSON data (serialiser)
from fastapi.encoders import jsonable_encoder

#Importing the DB functions we made in database.py
from server.database.post_database import (
    add_post,
    retrieve_post,
    retrieve_posts,
    delete_post,
    update_post
)

#Importing the Models we made in models/user.py
from server.models.post_models import (
    ErrorResponseModel,
    ResponseModel,
    PostSchema,
    UpdatePostModel,
)

#Initiate the router object
router = APIRouter()

@router.get('/', response_description='Posts recieved')
async def get_posts():
    posts = await retrieve_posts()
    if posts:
        return ResponseModel(posts, 'Post data retrieved successfully')
    return ResponseModel(posts, 'Returned an empty list')

#Get post by id
@router.get('/{id}', response_description='Post data retrieved successfully')
async def get_post_by_id(id):
    post = await retrieve_post(id)
    if post:
        return ResponseModel(post, 'Post data retrieved successfully')
    return ErrorResponseModel('An error occurred.', 404, "Post doesn't exist")

#Add a new post
@router.post('/', response_description='Post data added into the database') 
async def add_post_data(post: PostSchema = Body(...)):
    post = jsonable_encoder(post)
    new_post = await add_post(post)
    return ResponseModel(new_post, 'Post added successfully')

#Delete post by ID
@router.delete('/{id}')
async def delete_post_data(id: str):
    deleted_post = await delete_post(id)
    if deleted_post:
        return ResponseModel('Post with ID {} removed'.format(id), 'Post deleted successfully')
    return ErrorResponseModel('An error occurred', 404, 'Post with ID {} does not exist'.format(id))

#Update post by ID
@router.patch('/{id}')
async def update_post_data(id: str, req: UpdatePostModel = Body(...)):
    req = {k:v for k,v in req.dict().items() if v is not None} # Pardon? - need this explained
    updated_post = await update_post(id, req)
    if updated_post:
        return ResponseModel('Post with ID {} updated successfully'.format(id), 'Post updated successfully')
    return ErrorResponseModel('An error occurred', 404, 'There was an error updating data for post with ID {}'.format(id))