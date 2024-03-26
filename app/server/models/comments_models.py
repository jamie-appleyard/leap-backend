from typing import Optional
from pydantic import BaseModel, Field

class CommentsSchema(BaseModel):
    comment_body: str = Field(...)
    user_id: str = Field(...)
    votes: int = Field(...)

    class Config:
        schema_extra = {
            'comment_body': 'yada',
            'user_id': 'y1dayada981987',
            'votes': 0
        }

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message
    }

def ErrorResponseModel(error, code, message): 
    return {"error": error, "code": code, "message": message}