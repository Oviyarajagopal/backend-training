from sqlalchemy.orm import Session
import models


# =========================
# ✅ CREATE TASK (Ownership)
# =========================
def create_task(db: Session, task_data, current_user):
    new_task = models.Task(
        **task_data.dict(),
        user_id=current_user.id   # 🔐 assign owner
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


# =========================
# ✅ GET ALL TASKS (Isolation)
# =========================
def get_tasks(db: Session, current_user, priority: str = None):
    query = db.query(models.Task).filter(
        models.Task.user_id == current_user.id,
        models.Task.is_deleted == False
    )

    if priority:
        query = query.filter(models.Task.priority == priority)

    return query.all()


# =========================
# ✅ GET SINGLE TASK (Ownership)
# =========================
def get_task(db: Session, task_id: int, current_user):
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.is_deleted == False
    ).first()

    # 🔐 Hide existence (best practice)
    if not task or task.user_id != current_user.id:
        return None

    return task


# =========================
# ✅ UPDATE TASK (Only Owner)
# =========================
def update_task(db: Session, task_id: int, data, current_user):
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.is_deleted == False
    ).first()

    if not task or task.user_id != current_user.id:
        return None

    # 🔐 Only update allowed fields
    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task


# =========================
# ✅ DELETE TASK (Soft Delete)
# =========================
def delete_task(db: Session, task_id: int, current_user):
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.is_deleted == False
    ).first()

    if not task or task.user_id != current_user.id:
        return None

    task.is_deleted = True

    db.commit()

    return task