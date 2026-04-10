from sqlalchemy.orm import Session
import models


# ✅ CREATE TASK (assign owner)
def create_task(db: Session, task_data, current_user):
    new_task = models.Task(
        **task_data.dict(),
        user_id=current_user.id   # 🔐 ownership
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


# ✅ GET ALL TASKS (user isolation)
def get_tasks(db: Session, current_user, priority: str = None):
    query = db.query(models.Task).filter(
        models.Task.user_id == current_user.id,   # 🔐 only user's tasks
        models.Task.is_deleted == False
    )

    if priority:
        query = query.filter(models.Task.priority == priority)

    return query.all()


# ✅ GET SINGLE TASK (ownership check)
def get_task(db: Session, task_id: int, current_user):
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.is_deleted == False
    ).first()

    if not task or task.user_id != current_user.id:
        return None   # 🔐 hide data

    return task


# ✅ UPDATE TASK (only owner)
def update_task(db: Session, task_id: int, data, current_user):
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.is_deleted == False
    ).first()

    if not task or task.user_id != current_user.id:
        return None   # 🔐 not allowed

    for key, value in data.dict(exclude_unset=True).items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task


# ✅ DELETE TASK (only owner, soft delete)
def delete_task(db: Session, task_id: int, current_user):
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.is_deleted == False
    ).first()

    if not task or task.user_id != current_user.id:
        return None   # 🔐 not allowed

    task.is_deleted = True
    db.commit()

    return task