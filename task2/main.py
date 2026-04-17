from fastapi import FastAPI
from routers.task import router as task_router
from routers.comment import router as comment_router
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(task_router)
app.include_router(comment_router)
