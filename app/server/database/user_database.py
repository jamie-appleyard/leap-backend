import motor.motor_asyncio
from bson.objectid import ObjectId
from environs import Env

env = Env()
env.read_env()

MONGODB_URL = env('MONGODB_URL')
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client['leap-db']
users_col = db['users']

def user_helper(user):
    return {
        'id': str(user['_id']),
        'username': user['username'],
        'email': user['email'],
        'user_topics': user['user_topics']
    }

#ALL CRUD OPERATIONS
#Functions that interact directly with the database

#Fetch all users
async def retrieve_users():
    users = []
    async for user in users_col.find():
        users.append(user_helper(user))
    return users

#Get user by user ID
async def retrieve_user(id : str):
    try:
        user = await users_col.find_one({'_id' : ObjectId(id)})
    except:
        user = False
    if user:
        return user_helper(user)
    return False
    
#Add a new user
async def add_user(user_data : dict):
    user = await users_col.insert_one(user_data) #also insert_many()
    new_user = await users_col.find_one({'_id' : user.inserted_id})
    return user_helper(new_user)

#Delete a user
async def delete_user(id: str):
    user = await users_col.find_one({'_id' : ObjectId(id)})
    if user:
        await users_col.delete_one({'_id' : ObjectId(id)})
        return True
    
#Update a user
async def update_user(id: str, data: dict):
    if len(data) < 1:
        return False
    user = await users_col.find_one({'_id' : ObjectId(id)})
    if user:
        updated_user = await users_col.update_one({'_id' : ObjectId(id)}, {'$set': data})
        if updated_user:
            return True
        return False

async def add_topic_to_user_topics(id: str, new_topic: list):
    if len(new_topic) < 1:
        return False
    user = await users_col.find_one({'_id' : ObjectId(id)})
    if user:
        updated_user_topics = {'user_topics' :user['user_topics'] + new_topic}
        updated_user = await users_col.update_one({'_id' : ObjectId(id)}, {'$set': updated_user_topics})
        if updated_user:
            return True
        return False
