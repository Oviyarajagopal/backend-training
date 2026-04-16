from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Task
from schemas.comment import CommentCreate  # ignore if not needed

router = APIRouter()

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ CREATE TASK
@router.post("/tasks")
def create_task(title: str, db: Session = Depends(get_db)):
    user_id = 1  # temp

    new_task = Task(
        title=title,
        user_id=user_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task