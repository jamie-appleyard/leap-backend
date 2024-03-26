import motor.motor_asyncio
from bson.objectid import ObjectId
from environs import Env

env = Env()
env.read_env()

MONGODB_URL = env('MONGODB_URL')
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client['leap-db']
topic_col = db['topic']

def topic_helper(topic):
    return {
        'id': str(topic['_id']),
        'topic_name': topic['topic_name'],
        'summary': topic['summary'],
        'pond_id': str(topic['pond_id'])
    }

async def retrieve_topics():
    topics = []
    async for topic in topic_col.find():
        topics.append(topic_helper(topic))
    return topics

async def retrieve_topic(id : str):
    topic = await topic_col.find_one({'_id' : ObjectId(id)})
    if topic:
        return topic_helper(topic)
    
async def add_topic(topic_data : dict):
    topic = await topic_col.insert_one(topic_data)
    new_topic = await topic_col.find_one({'_id' : topic.inserted_id})#unsure about inserted?
    return topic_helper(new_topic)

async def update_topic(id: str, data: dict):
    if len(data) < 1:
        return False
    topic = await topic_col.find_one({"_id": ObjectId(id)})
    if topic:
        updated_topic = await topic_col.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_topic:
            return True
        return False
    
async def delete_topic(id: str):
    topic = await topic_col.find_one({"_id": ObjectId(id)})
    if topic:
        await topic_col.delete_one({"_id": ObjectId(id)})
        return True