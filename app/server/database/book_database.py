import motor.motor_asyncio
from bson.objectid import ObjectId
from environs import Env
from ..utils.books_api import create_books

env = Env()
env.read_env()

MONGODB_URL = env('MONGODB_URL')
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client['leap-db']
book_col = db['book']
topic_col = db['topic']

def book_helper(book):
    return {
        'id': str(book['_id']),
        'topic_id': str(book['topic_id']),
        'books': book['books']
    }
    
async def retrieve_books():
    books = []
    async for book in book_col.find():
        books.append(book_helper(book))
    return books

async def add_books(book_data: dict):
    try:
        book = await book_col.insert_one(book_data)
    except:
        return False
    new_book = await book_col.find_one({'_id': book.inserted_id})
    return book_helper(new_book)

async def retrieve_books_by_topic_id(topic_id: str):
    topic = await topic_col.find_one({'_id': ObjectId(topic_id)})
    if topic:
        books = await book_col.find_one({'topic_id': topic_id})
        if books:
            return book_helper(books)
        else:
            return []
    else:
        return False

async def generate_books(topic_id):
    topic = await topic_col.find_one({'_id': ObjectId(topic_id)})

    if topic:   
        topic_name = topic["topic_name"]
        books = await create_books(topic_name)
        post_books = {
            'topic_id': topic_id,
            'books': books
        }
        new_book = await add_books(post_books)
        return new_book
    else:
        return False
