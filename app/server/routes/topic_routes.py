from fastapi import APIRouter, Body


from fastapi.encoders import jsonable_encoder

from server.database.topic_database import (
    retrieve_topic,
    add_topic
)

from server.models.topic_models import (
    ResposeModel,
    ErrorResponseModel,
    TopicSchema
)

router = APIRouter()

@router.get('/{id}', response_description='Topic data retrieved successfully')
async def get_topic_by_id(id):
    topic = await retrieve_topic(id)
    if topic:
        return ResposeModel(topic, 'Topic data retrieved successfully')
    return ErrorResponseModel('An error occurred.', 404, 'topic does not exist')

@router.post('/', response_description='Topic data added into the database')
async def add_topic_data(topic: TopicSchema = Body(...)):
    topic = jsonable_encoder(topic)
    new_topic = await add_topic(topic)
    return ResposeModel(new_topic, 'Topic added successfully')