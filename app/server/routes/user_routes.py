from fastapi import APIRouter, Body

#Translate python dictionaries in to JSON data (serialiser)
from fastapi.encoders import jsonable_encoder

#Importing the DB functions we made in database.py
from server.database.user_database import (
    add_user,
    retrieve_user,
    retrieve_users,
)

#Importing the Models we made in models/user.py
from server.models.user_models import (
    ErrorResponseModel,
    ResponseModel,
    UserSchema,
    #UpdateUserModel
)

#Initiate the router object
router = APIRouter()

@router.get('/', response_description='Users recieved')
async def get_users():
    users = await retrieve_users()
    if users:
        return ResponseModel(users, 'User data retrieved successfully')
    return ResponseModel(users, 'Returned an empty list')

#Get user by id
@router.get('/{id}', response_description='User data retrieved successfully')
async def get_user_by_id(id):
    user = await retrieve_user(id)
    if user:
        return ResponseModel(user, 'User data retrieved successfully')
    return ErrorResponseModel('An error occurred.', 404, "User doesn't exist")

#Add a new user
@router.post('/', response_description='User data added into the database') 
async def add_user_data(user: UserSchema = Body(...)):
    user = jsonable_encoder(user)
    new_user = await add_user(user)
    return ResponseModel(new_user, 'User added successfully')