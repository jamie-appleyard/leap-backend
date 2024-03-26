import motor.motor_asyncio
from bson.objectid import ObjectId
from environs import Env

env = Env()
env.read_env()

MONGODB_URL = env('MONGODB_URL')
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client['leap-db']
comment_col = db['comment']

def comment_helper(comment):
    return {
        'comment_body': str(comment['comment_body']),
        'user_id': str(comment['user_id']),
        'votes': int(comment['votes'])
    }

#Fetch all comments
async def retrieve_comments():
    comments = []
    async for comment in comment_col.find():
        comments.append(comment_helper(comment))
    return comments

#Fetch comment by ID
async def retrieve_comment(id : str):
    comment = await comment_col.find_one({'_id' : ObjectId(id)})
    if comment:
        return comment_helper(comment)

async def update_comment(id: str, data: dict):
    if len(data) < 1:
        return False
    comment = await comment_col.find_one({"_id": ObjectId(id)})
    if comment:
        updated_comment = await comment_col.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_comment:
            return True
        return False

#Add a new comment
async def add_comment(comment_data : dict):
    comment = await comment_col.insert_one(comment_data) #also insert_many()
    new_comment = await comment_col.find_one({'_id' : comment.inserted_id})
    return comment_helper(new_comment)

#Delete a comment by id
async def delete_comment(id: str):
    comment = await comment_col.find_one({'_id': ObjectId(id)})
    if comment:
        await comment_col.delete_one({'_id': ObjectId(id)})
        return True
