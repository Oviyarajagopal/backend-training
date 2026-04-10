from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, SessionLocal
from utils import hash_password
from utils import verify_password, create_access_token
from routers import task_routers  # your task routes

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# 🔹 Dependency (DB)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔹 REGISTER API
@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # 🔸 Check if email already exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

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

    return {
        "message": "User registered successfully",
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email
        }
    }


# 🔹 INCLUDE TASK ROUTES
app.include_router(task_routers.router)

@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    
    # 🔸 Check if user exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # 🔸 Verify password
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # 🔸 Create JWT token
    access_token = create_access_token(
        data={"user_id": db_user.id}
    )

    return {
        "access_token": access_token
    }