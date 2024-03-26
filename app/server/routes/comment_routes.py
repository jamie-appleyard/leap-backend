from fastapi import APIRouter, Body

from fastapi.encoders import jsonable_encoder

from server.models.comment_models import (
    CommentSchema,
    ResponseModel,
    ErrorResponseModel
)

from server.database.comment_database import (
    delete_comment
)

router = APIRouter()

@router.delete('/{id}')
async def delete_comment_data(id:str):
    deleted_comment = await delete_comment(id)
    if deleted_comment:
        return ResponseModel('Comment with ID: {} deleted successfully.'.format(id), 'Comment deleted successfully')
