from fastapi import APIRouter, Body


from fastapi.encoders import jsonable_encoder

from ..database.topic_database import (
    retrieve_topic,
    retrieve_topics,
    add_topic,
    update_topic,
    delete_topic
)

from ..models.topic_models import (
    ResponseModel,
    ErrorResponseModel,
    TopicSchema,
    UpdateTopicModel
)

router = APIRouter()

@router.get('/', response_description='Topics receieved')
async def get_topics():
    topics = await retrieve_topics()
    if topics:
        return ResponseModel(topics, 'Topics data retrieved successfully')
    return ResponseModel(topics, 'Returned an empty list')

@router.get('/{id}', response_description='Topic data retrieved successfully')
async def get_topic_by_id(id):
    topic = await retrieve_topic(id)
    if topic:
        return ResponseModel(topic, 'Topic data retrieved successfully')
    return ErrorResponseModel('An error occurred.', 404, 'topic does not exist')

@router.post('/', response_description='Topic data added into the database')
async def add_topic_data(topic: TopicSchema = Body(...)):
    topic = jsonable_encoder(topic)
    new_topic = await add_topic(topic)
    if new_topic:
        return ResponseModel(new_topic, 'Topic added successfully')
    return ErrorResponseModel('An error occurred.', 404, 'topic cannot be posted')

@router.put("/{id}")
async def update_topic_data(id: str, req: UpdateTopicModel = Body(...)):
    req = {k: v for k, v in req.model_dump().items() if v is not None}
    updated_topic = await update_topic(id, req)
    if updated_topic:
        return ResponseModel(
            "topic with ID: {} update successful".format(id),
            'Topic updated Successfully'
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "error topic does not exist"
    )

@router.delete("/{id}", response_description="topic data deleted from database")
async def delete_topic_data(id: str):
    deleted_topic = await delete_topic(id)
    if deleted_topic:
        return ResponseModel(
            "topic with ID: {} removed".format(id), "topic deleted successfully"
        )
    return ErrorResponseModel(
        "An error occcurred", 404, "topic with id {0} does not exist".format(id)
    )
