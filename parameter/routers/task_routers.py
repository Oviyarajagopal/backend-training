from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import schemas
from services import task_service
from utils import get_current_user, get_db

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# =========================
# ✅ CREATE TASK (Protected)
# =========================
@router.post("/")
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return task_service.create_task(db, task, current_user)


# =========================
# ✅ GET ALL TASKS (User Isolation)
# =========================
@router.get("/")
def get_tasks(
    priority: str = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return task_service.get_tasks(db, current_user, priority)


# =========================
# ✅ GET SINGLE TASK (Ownership)
# =========================
@router.get("/{id}")
def get_task(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    task = task_service.get_task(db, id, current_user)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


# =========================
# ✅ UPDATE TASK (Only Owner)
# =========================
@router.put("/{id}")
def update_task(
    id: int,
    data: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    result = task_service.update_task(db, id, data, current_user)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed"
        )

    return {"message": "Task updated successfully"}


# =========================
# ✅ DELETE TASK (Soft Delete)
# =========================
@router.delete("/{id}")
def delete_task(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    result = task_service.delete_task(db, id, current_user)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed"
        )

    return {"message": "Task deleted successfully"}