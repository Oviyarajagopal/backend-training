from fastapi import APIRouter, Depends,HTTPException
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

@router.post("/tasks")
def create_task(title: str, db: Session = Depends(get_db)):
    task = Task(title=title)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.get("/tasks/{id}")
def get_task(id: int, db: Session = Depends(get_db)):

    task = db.query(Task).filter(Task.id == id).first()

    if not task:
        raise HTTPException(404, "Task not found")

    return {
        "id": task.id,
        "title": task.title,
        "comments": [
            {
                "content": c.content,
                "user": c.user.name
            }
            for c in task.comments if not c.is_deleted
        ]
    }