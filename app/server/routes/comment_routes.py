from fastapi import APIRouter, Body

from fastapi.encoders import jsonable_encoder

from server.database.comment_database import (
    retrieve_comments,
    retrieve_comment
) 

from server.models.comment_models import (
    ErrorResponseModel,
    ResponseModel,
    CommentSchema
)

router = APIRouter()

@router.get('/', response_description='Users recieved')
async def get_comments():
    comments = await retrieve_comments()
    if comments:
        return ResponseModel(comments, 'Comments data retrieved successfully')
    return ResponseModel(comments, 'Returned an empty list')

@router.get('/{id}', response_description='Topic data retrieved successfully')
async def get_comment_by_id(id):
    comment = await retrieve_comment(id)
    if comment:
        return ResponseModel(comment, 'Comment data retrieved successfully')
    return ErrorResponseModel('An error occurred.', 404, 'Comment does not exist')