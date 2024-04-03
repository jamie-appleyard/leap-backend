import motor.motor_asyncio
from bson.objectid import ObjectId
from environs import Env
from ..utils.cohere_api import sum_gen

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
        'summary': topic['summary']
    }

async def retrieve_topics():
    topics = []
    async for topic in topic_col.find():
        topics.append(topic_helper(topic))
    return topics

async def retrieve_topic(id : str):
    try:
        topic = await topic_col.find_one({'_id' : ObjectId(id)})
    except:
        topic = False
    if topic:
        return topic_helper(topic)
    return False
    
async def add_topic(topic_data : dict):
    try:
        topic = await topic_col.insert_one(topic_data)
    except:
        return False
    new_topic = await topic_col.find_one({'_id' : topic.inserted_id})#unsure about inserted?
    return topic_helper(new_topic)

async def update_topic(id: str, data: dict):
    if len(data) < 1:
        return False
    try:
        topic = await topic_col.find_one({"_id": ObjectId(id)})
    except:
        topic = False
    if topic:
        updated_topic = await topic_col.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_topic:
            return True
    return False

async def generate_topic(topic):
    topic = topic.title()
    topic = topic.replace('+', ' ')
    topic_summary = sum_gen(topic)
    post_topic = {
        'topic_name': topic,
        'summary': topic_summary
    }
    new_topic = await add_topic(post_topic)
    return new_topic
    
async def delete_topic(id: str):
    try:
        topic = await topic_col.find_one({"_id": ObjectId(id)})
    except:
        topic = False
    if topic:
        await topic_col.delete_one({"_id": ObjectId(id)})
        return True