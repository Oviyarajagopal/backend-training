from fastapi import Header
from utils import verify_token
from fastapi import Depends, Header
from sqlalchemy.orm import Session
from fastapi import HTTPException
import models
from database import get_db

def get_current_user(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    # 🔴 Check header exists
    if not authorization:
        raise HTTPException(status_code=401, detail="Token missing")

    # 🔴 Format: Bearer <token>
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid token format")
    except:
        raise HTTPException(status_code=401, detail="Invalid token format")

    # 🔐 Decode token
    user_id = verify_token(token)

    # 🔍 Get user from DB
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user