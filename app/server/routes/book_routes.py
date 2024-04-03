from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from ..database.book_database import (
    retrieve_books,
    retrieve_books_by_topic_id,
    generate_books,
    add_books
)

from ..models.book_models import (
    ResponseModel,
    ErrorResponseModel
)

router = APIRouter()

@router.get('/', response_description='Books received')
async def get_books():
    books = await retrieve_books()
    if books:
        return ResponseModel(books, 'Books data retrieved successfully')
    return ResponseModel(books, 'Returned an empty list')

@router.get('/{topic_id}', response_description='Books received for topic')
async def get_books_by_topic(topic_id: str):
    books = await retrieve_books_by_topic_id(topic_id)
    if books or books == []:
        return ResponseModel(books, 'Books data retrieved successfully')
    else:
        return ErrorResponseModel('An error occurred.', 404, "topic ID doesn't exist")

@router.post("/{topic_id}", response_description="New books generated")
async def generate_new_books(topic_id: str):
    new_books = await generate_books(topic_id)
    if new_books:
        return ResponseModel(new_books, 'Books created successfully')
    return ErrorResponseModel(
        "An error occurred", 500, 'New books generation failed.'
    )