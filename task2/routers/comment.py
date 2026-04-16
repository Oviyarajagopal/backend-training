from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from database import SessionLocal
from models import Comment, Task
from schemas.comment import CommentCreate
from dependencies.auth import get_current_user
router = APIRouter()

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ CREATE COMMENT
@router.post("/tasks/{task_id}/comments")
def create_comment(task_id: int, comment: CommentCreate, db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    
    # 🔍 Check task exists
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")


    # 2. Create comment
    db_comment = Comment(
        content=comment.content,
        task_id=task_id,
        user_id=current_user.id   # from token
    )

    # 3. Save to DB
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)

    return {
        "message": "Comment created successfully",
        "comment_id": db_comment.id
    }

@router.get("/tasks/{task_id}/comments")
def get_comments(
    task_id: int,
    db: Session = Depends(get_db)
):
    
    # 1. Check if task exists
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # 2. Get comments
    comments = db.query(Comment).filter(Comment.task_id == task_id).all()

    # 3. Format response
    return [
        {
            "content": c.content,
            "created_at": c.created_at,
            "user": c.user.name   # 🔥 relationship usage
        }
        for c in comments
    ]

@router.put("/comments/{id}")
def update_comment(
    id: int,
    request: CommentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    
    comment = db.query(Comment).filter(Comment.id == id).first()

    if not comment:
        raise HTTPException(404, "Comment not found")

    # 🔥 Ownership check
    if comment.user_id != current_user.id:
        raise HTTPException(403, "Not authorized")

    comment.content = request.content
    db.commit()

    return {"message": "Updated successfully"}