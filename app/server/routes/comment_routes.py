from fastapi import APIRouter, Body

from fastapi.encoders import jsonable_encoder

from server.database.comment_database import (
    update_comment
)

from server.models.comment_models import (
    ResponseModel,
    ErrorResponseModel,
    UpdateCommentModel
)

router = APIRouter()

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