from typing import Optional
from pydantic import BaseModel, Field

class PostSchema(BaseModel):
    topic_id: str = Field(...)
    post_body: str = Field(...)
    title: str = Field(...)
    user_id: str = Field(...)
    votes: int = Field(default=0)
    post_image: str = Field(...)
    type: list = Field(...)

    class Config:
        scheme_extra = {
            'topic_id': '78ewsdahucijonhcu',
            'post_body': 'This is a new post!',
            'title': 'My Title',
            'user_id': '7dshudjakbfahy',
            'votes': 0,
            'post_image': 'https://my-image.jpeg',
            'type': [],
            }

class UpdatePostModel(BaseModel):
    title: Optional[str]
    post_body: Optional[str]
    post_image: Optional[str]
    type: Optional[list]
            

def ResponseModel(data, message): #Lift up to parent and import DRY
    return {
        "data": [data],
        "code": 200,
        "message": message
    }

def ErrorResponseModel(error, code, message): #Lift up to parent and import DRY
    return {"error": error, "code": code, "message": message}