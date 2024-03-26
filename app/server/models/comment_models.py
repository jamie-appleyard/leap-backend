from typing import Optional
from pydantic import BaseModel, Field

class CommentSchema(BaseModel):
    comment_body: str = Field(...)
    user_id: str = Field(...)
    votes: int = Field(...)

    class Config:
        schema_extra = {
            'comment_body': 'yada',
            'user_id': 'y1dayada981987',
            'votes': 0
        }

class UpdateCommentModel(BaseModel):
    comment_body: Optional[str]
    user_id: Optional[str]
    votes: Optional[int]

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message
    }

def ErrorResponseModel(error, code, message): 
    return {"error": error, "code": code, "message": message}
