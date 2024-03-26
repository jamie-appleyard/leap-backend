from fastapi import FastAPI

from server.routes.user_routes import router as UserRouter
from server.routes.topic_routes import router as TopicRouter

app = FastAPI()

app.include_router(UserRouter, tags=['user'], prefix='/user')

app.include_router(TopicRouter, tags=['topic'], prefix='/topic')

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}