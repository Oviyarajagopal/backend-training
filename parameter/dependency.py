from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from utils import verify_token
import models

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise Exception()
    except:
        raise HTTPException(status_code=401, detail="Invalid token format")

    user_id = verify_token(token)

    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user