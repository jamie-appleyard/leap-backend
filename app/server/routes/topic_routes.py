from fastapi import APIRouter, Body


from fastapi.encoders import jsonable_encoder

from server.database.topic_database import (
    retrieve_topic
)

from server.models.topic_models import (
    ResposeModel,
    ErrorResponseModel
)

router = APIRouter()

@router.get('/{id}', response_description='Topic data retrieved successfully')
async def get_topic_by_id(id):
    topic = await retrieve_topic(id)
    if topic:
        return ResposeModel(topic, 'Topic data retrieved successfully')
    return ErrorResponseModel('An error occurred.', 404, 'topic does not exist')