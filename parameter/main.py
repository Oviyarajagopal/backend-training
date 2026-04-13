from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from database import engine
from utils import hash_password, verify_password, create_access_token, get_db
from routers import task_routers

# 🔹 Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# =========================
# 🔹 REGISTER API
# =========================
@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # 🔸 Check if email already exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # 🔸 Hash password
    hashed_password = hash_password(user.password)

    # 🔸 Create user
    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_password
    )

    # 🔸 Save to DB
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# =========================
# 🔹 LOGIN API
# =========================
@app.post("/login", response_model=schemas.TokenResponse)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):

    # 🔸 Check if user exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or password"
        )

    # 🔸 Verify password
    if not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or password"
        )

    # 🔸 Create JWT token
    access_token = create_access_token(
        data={"user_id": db_user.id}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# =========================
# 🔹 INCLUDE TASK ROUTES
# =========================
app.include_router(task_routers.router)