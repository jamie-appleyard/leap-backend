from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes.user_routes import router as UserRouter
from .routes.topic_routes import router as TopicRouter
from .routes.comment_routes import router as CommentRouter
from .routes.post_routes import router as PostRouter

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://0.0.0.0:8000",
    "http://0.0.0.0:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(UserRouter, tags=['user'], prefix='/user')
app.include_router(TopicRouter, tags=['topic'], prefix='/topic')
app.include_router(PostRouter, tags=['post'], prefix='/post')
app.include_router(CommentRouter, tags=['comment'], prefix='/comment')

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}