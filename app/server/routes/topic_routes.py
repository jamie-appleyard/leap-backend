from fastapi import APIRouter, Body


from fastapi.encoders import jsonable_encoder

from server.database.topic_database import (
    retrieve_topic,
    add_topic,
    update_topic
)

from server.models.topic_models import (
    ResponseModel,
    ErrorResponseModel,
    TopicSchema,
    UpdateTopicModel
)

router = APIRouter()

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
    return ResponseModel(new_topic, 'Topic added successfully')

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
        "error updating topic"
    )
