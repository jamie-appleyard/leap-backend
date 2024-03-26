from fastapi import FastAPI

from server.routes.user_routes import router as UserRouter
from server.routes.post_routes import router as PostRouter

app = FastAPI()

app.include_router(UserRouter, tags=['user'], prefix='/user')

app.include_router(PostRouter, tags=['post'], prefix='/post')

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}