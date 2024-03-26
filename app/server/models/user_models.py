from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class UserSchema(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    # profile_picture: str = Optional[str]#How to set as a file field and have a default
    # user_topics: dict = Optional[dict]
    # user_ponds: dict = Optional[dict]

    class Config:
        scheme_extra = {
            'username': "Bob",
            'email' : 'japple@japple.com',
            'profile_picture': 'hello.jpeg',
            'user_topics' : [],
            'user_ponds' : []
        }

class UpdateUserModel(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]

def ResponseModel(data, message): #Lift up to parent and import DRY
    return {
        "data": [data],
        "code": 200,
        "message": message
    }

def ErrorResponseModel(error, code, message): #Lift up to parent and import DRY
    return {"error": error, "code": code, "message": message}