from fastapi import APIRouter, Body

from fastapi.encoders import jsonable_encoder

from ..database.comment_database import (
    retrieve_comments,
    retrieve_comment,
    update_comment,
    add_comment,
    delete_comment
) 

from ..models.comment_models import (
    ErrorResponseModel,
    ResponseModel,
    UpdateCommentModel,
    CommentSchema
)

router = APIRouter()

#Get all comments
@router.get('/', response_description='Comments recieved')
async def get_comments():
    comments = await retrieve_comments()
    if comments:
        return ResponseModel(comments, 'Comments data retrieved successfully')
    return ResponseModel(comments, 'Returned an empty list')

#Get comment by ID
@router.get('/{id}', response_description='Comment data retrieved successfully')
async def get_comment_by_id(id):
    comment = await retrieve_comment(id)
    if comment:
        return ResponseModel(comment, 'Comment data retrieved successfully')
    return ErrorResponseModel('An error occurred.', 404, 'Comment does not exist')

#Update a comment by ID
@router.put("/{id}")
async def update_comment(id: str, req: UpdateCommentModel = Body(...)):
    req = {k: v for k, v in req.model_dump().items() if v is not None}
    updated_comment = await update_comment(id, req)
    if updated_comment:
        return ResponseModel(
            "Comment with ID: {} update successful".format(id),
            "Comment name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the comment data"
    )

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
