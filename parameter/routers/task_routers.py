from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import schemas
from services import task_service
from utils import get_current_user

router = APIRouter()

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ CREATE TASK (Protected)
@router.post("/tasks")
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return task_service.create_task(db, task, current_user)


# ✅ GET ALL TASKS (User Isolation)
@router.get("/tasks")
def get_tasks(
    priority: str = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    tasks = task_service.get_tasks(db, current_user, priority)
    return tasks


# ✅ GET SINGLE TASK (Ownership Check)
@router.get("/tasks/{id}")
def get_task(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    task = task_service.get_task(db, id, current_user)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


# ✅ UPDATE TASK (Only Owner)
@router.put("/tasks/{id}")
def update_task(
    id: int,
    data: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    result = task_service.update_task(db, id, data, current_user)

    if not result:
        raise HTTPException(status_code=403, detail="Not allowed")

    return {"message": "Updated"}


# ✅ DELETE TASK (Only Owner)
@router.delete("/tasks/{id}")
def delete_task(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    result = task_service.delete_task(db, id, current_user)

    if not result:
        raise HTTPException(status_code=403, detail="Not allowed")

    return {"message": "Deleted (soft)"}