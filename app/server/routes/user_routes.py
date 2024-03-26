from fastapi import APIRouter, Body

#Translate python dictionaries in to JSON data (serialiser)
from fastapi.encoders import jsonable_encoder

#Importing the DB functions we made in database.py
from server.database.user_database import (
    add_user,
    retrieve_user,
    retrieve_users,
    delete_user,
    update_user
)

#Importing the Models we made in models/user.py
from server.models.user_models import (
    ErrorResponseModel,
    ResponseModel,
    UserSchema,
    UpdateUserModel
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

#Delete user by ID
@router.delete('/{id}')
async def delete_user_data(id: str):
    deleted_user = await delete_user(id)
    if deleted_user:
        return ResponseModel('User with ID {} removed'.format(id), 'User deleted successfully')
    return ErrorResponseModel('An error occurred', 404, 'Student with ID {} does not exist'.format(id))

#Update user by ID
@router.patch('/{id}')
async def update_user_data(id: str, req: UpdateUserModel = Body(...)):
    req = {k:v for k,v in req.dict().items() if v is not None}
    print(req)
    updated_user = await update_user(id, req)
    if updated_user:
        return ResponseModel('User with ID {} updated successfully'.format(id), 'User updated successfully')
    return ErrorResponseModel('An error occurred', 404, 'There was an error updating data for student with ID {}'.format(id))
