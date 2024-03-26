from typing import Optional
from pydantic import BaseModel, Field

class TopicSchema(BaseModel):
    topic_name: str = Field(...)
    summary: str = Field(...)
    pond_id: str = Field(...)
    # sub_data: dict = Optional[dict]

    class Config:
        schema_extra = {
            'topic_name': 'stonemasonry',
            'summary': 'cutting rocks',
            'pond_id': 'dsdasd45465s4da6s5d46as54d6',
            'sub_data': []
        }

class UpdateTopicModel(BaseModel):
    topic_name: Optional[str]
    summary: Optional[str]
    pond_id: Optional[str]
    # sub_data: dict = Optional[dict]

    class Config:
        schema_extra = {
            'topic_name': 'stonemasonry',
            'summary': 'cutting rocks',
            'pond_id': 'dsdasd45465s4da6s5d46as54d6',
            'sub_data': []
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message
    }

def ErrorResponseModel(error, code, message): 
    return {"error": error, "code": code, "message": message}
    