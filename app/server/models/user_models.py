from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

class UserSchema(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    user_topics: List[str] = []
    # user_ponds: dict = Optional[dict]

    class Config:
        scheme_extra = {
            'username': "Bob",
            'password': "bobrocks123",
            'email' : 'japple@japple.com'
        }

class UpdateUserModel(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    user_topics: Optional[List]

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message
    }

def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}