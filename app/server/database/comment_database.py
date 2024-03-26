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