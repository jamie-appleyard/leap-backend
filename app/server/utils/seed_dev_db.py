import motor.motor_asyncio
from bson.objectid import ObjectId
from environs import Env
import json
import asyncio
from cohere_api import sum_gen
import random

env = Env()
env.read_env()

MONGODB_URL = env('MONGODB_URL')
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client['leap-db']
users_col = db['users']
topics_col = db['topic']
posts_col = db['posts']
comments_col = db['comment']

#Function to empty any existing docs out of a given collection
async def empty_col(col, col_string):
    try:
        await col.delete_many({})
    except:
        print('Failed to delete all {} documents'.format(col_string))

#Function that adds a set of objects in an array to a col
async def add_test_data_to_col(col, col_string, test_data):
    try:
        await col.insert_many(test_data)
    except:
        print('Failed to add {} test data'.format(col_string))

async def delete_add_cycle(col, col_string, test_data):
    await empty_col(col, col_string)
    await add_test_data_to_col(col, col_string, test_data)

#Main function to run a full database purge and repopulation with fresh data
async def main():
    users_task = asyncio.create_task(
        delete_add_cycle(users_col, 'users', user_data)
    )
    topics_task = asyncio.create_task(
        delete_add_cycle(topics_col, 'topics', topics_data)
    )
    complete_post_data = asyncio.create_task(
        add_user_topic_to_posts(posts_data)
    )
    complete_comment_data = asyncio.create_task(
        add_user_post_to_comments(comments_data)
    )

    await users_task
    await topics_task

    new_posts_data = await complete_post_data

    posts_task = asyncio.create_task(
        delete_add_cycle(posts_col, 'posts', new_posts_data)
    )
    
    await posts_task

    new_comments_data = await complete_comment_data

    comments_task = asyncio.create_task(
        delete_add_cycle(comments_col, 'comments', new_comments_data)
    )

    await comments_task

    print('Seeding completed.')

#TEST USER DATA
users_json = open('test-data/test_users.json')
user_data = json.load(users_json)
users_json.close()

for user in user_data:
    user['user_topics'] = []
    
def user_helper(user):
    return {
        'id': str(user['_id']),
        'username': user['username'],
        'email': user['email'],
        'user_topics': user['user_topics']
    }

async def get_users():
    users = []
    async for user in users_col.find():
        users.append(user_helper(user))
    return users

#TEST TOPICS DATA
topics_json = open('test-data/test_topics.json')
topics_data = json.load(topics_json)
topics_json.close()

#CREATE REAL SUMMARIES FOR TOPICS DATA
topics_data = topics_data[:20]
for topic in topics_data:
    topic_name = topic['topic_name']
    topic['summary'] = sum_gen(topic['topic_name'])


def topic_helper(topic):
    return {
        'id': str(topic['_id']),
        'topic_name': topic['topic_name'],
        'summary': topic['summary']
    }

async def get_topics():
    topics = []
    async for topic in topics_col.find():
        topics.append(topic_helper(topic))
    return topics

#TEST POSTS DATA
posts_json = open('test-data/test_posts.json')
posts_data = json.load(posts_json)
posts_json.close()

#Function that adds a user_id, topic_id and type to a post
async def add_user_topic_to_posts(post_data):
    users = await get_users()
    topics = await get_topics()
    new_post_data = []
    while len(users) == 0 or len(topics) == 0:
        if len(users) == 0:
            users = await get_users()
        if len(topics) == 0:
            topics = await get_topics()
    for post in post_data:
        new_post = post
        user_index = random.randint(0, len(users)-1)
        new_post['user_id'] = users[user_index]['id']
        topic_index = random.randint(0, len(topics)-1)
        new_post['topic_id'] = topics[topic_index]['id']
        new_post['type'] = 'post'
        new_post_data.append(new_post)
    return new_post_data

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

async def get_posts():
    posts = []
    async for post in posts_col.find():
        posts.append(post_helper(post))
    return posts

#TEST COMMENT DATA
comments_json = open('test-data/test_comments.json')
comments_data = json.load(comments_json)
comments_json.close()

def comment_helper(comment):
    return {
        'id' : str(comment['_id']),
        'comment_body': str(comment['comment_body']),
        'user_id': str(comment['user_id']),
        'votes': int(comment['votes']),
        'post_id': str(comment['post_id'])
    }

#Function that adds a user_id and post_id to each comment
async def add_user_post_to_comments(comment_data):
    users = await get_users()
    posts = await get_posts()
    while len(users) == 0 or len(posts) ==0:
        if len(users) == 0:
            users = await get_users()
        if len(posts) == 0:
            posts = await get_posts()
    new_comment_data = []
    for comment, user, posts in zip(comment_data, users, posts):
        new_comment = comment   
        new_comment['user_id'] = user['id']
        new_comment['post_id'] = posts['id']
        new_comment_data.append(new_comment)
    return new_comment_data

#Decorator function to re-seed the test DB before each test runs
def seed_test_data(func):
    def wrapper():
        asyncio.run(main())
        func()
    return wrapper

#Run the main function
asyncio.run(main())