import motor.motor_asyncio
from bson.objectid import ObjectId
from environs import Env

env = Env()
env.read_env()

MONGODB_URL = env('MONGODB_URL')
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client['leap-db']
post_col = db['posts']

#helpers function [function_name]():

def post_helper(post):
    return {
        'id': str(post['_id']),
        'topic_id': str(post['topic_id']),
        'title': post['title'],
        'user_id': str(post['user_id']),
        'votes': int(post['votes']),
        'post_image': str(post['post_image']),
        'type': str(post['type'])
    }

#ALL CRUD OPERATIONS
#Functions that interact directly with the database

#Fetch all posts
async def retrieve_posts():
    posts = []
    async for post in post_col.find():
        posts.append(post_helper(post))
    return posts

#Get post by post ID
async def retrieve_post(id : str):
    post = await post_col.find_one({'_id' : ObjectId(id)})
    if post:
        return post_helper(post)
    
#Add a new post
async def add_post(post_data : dict):
    post = await post_col.insert_one(post_data)
    new_post = await post_col.find_one({'_id' : post.inserted_id})
    return post_helper(new_post)

#Delete post by post ID
async def delete_post(id: str):
    post = await post_col.find_one({'_id' : ObjectId(id)})
    if post:
        await post_col.delete_one({'_id' : ObjectId(id)})
        return True
    
#Patch a post by ID
async def update_post(id: str, data: dict):
    if len(data) < 1:
        return False
    user = await post_col.find_one({'_id' : ObjectId(id)})
    if user:
        updated_post = await post_col.update_one({'_id' : ObjectId(id)}, {'$set': data})
        if updated_post:
            return True
        return False