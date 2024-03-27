import motor.motor_asyncio
from bson.objectid import ObjectId
from environs import Env
import json

env = Env()
env.read_env()

MONGODB_URL = env('MONGODB_URL')
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client['leap-db']
users_col = db['users']

f = open('test-data/test_users.json')

user_data = json.load(f)

for i in user_data:
    users_col.insert_many()
 
f.close()


# def user_helper(user):
#     return {
#         'id': str(user['_id']),
#         'username': user['username'],
#         'email': user['email']
#     }

# async def add_test_users(user_data : dict):
#     user = await users_col.insert_one(user_data) #also insert_many()
#     new_user = await users_col.find_one({'_id' : user.inserted_id})
#     return user_helper(new_user)