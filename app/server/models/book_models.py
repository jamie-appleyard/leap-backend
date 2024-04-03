from typing import Optional, List
from pydantic import BaseModel, Field

class BookSchema(BaseModel):
    topic_id: str = Field(...)
    books: List[str] = []
    
    class Config:
        schema_extra = {
            'topic_id': '6662ydhwsjidask',
            'books': ['book 1', 'book 2']
        }
        
def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message
    }

def ErrorResponseModel(error, code, message): 
    return {"error": error, "code": code, "message": message}
