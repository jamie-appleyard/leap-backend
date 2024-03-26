from fastapi import APIRouter, Body

from fastapi.encoders import jsonable_encoder

#Importing the DB functions we made in database.py
from server.database.comment_database import (
    add_comment,
    delete_comment
)

#Importing the Models we made in models/user.py
from server.models.comment_models import (
    ErrorResponseModel,
    ResponseModel,
    CommentSchema,
)

#Initiate the router object
router = APIRouter()

# Add a new comment
@router.post('/', response_description='Comment data added into the database') 
async def add_comment_data(comment: CommentSchema = Body(...)):
    comment = jsonable_encoder(comment)
    new_comment = await add_comment(comment)
    return ResponseModel(add_comment, 'Comment added successfully')

#Delete a comment by ID
@router.delete('/{id}')
async def delete_comment_data(id:str):
    deleted_comment = await delete_comment(id)
    if deleted_comment:
        return ResponseModel('Comment with ID: {} deleted successfully.'.format(id), 'Comment deleted successfully')
