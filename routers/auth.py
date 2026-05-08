from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime, timedelta

from database import SessionLocal
from models.user import User
from schemas.user import UserCreate
from utils.hashing import hash_password, verify_password
from dependencies import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# REGISTER
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    role = "user"

    # ADMIN USER
    if user.username == "admin":
        role = "admin"

    new_user = User(
        username=user.username,
        hashed_password=hash_password(user.password),
        role=role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully"
    }


# LOGIN
@router.post("/login")
def login(data: UserCreate, db: Session = Depends(get_db)):

    user = db.query(User).filter(
        User.username == data.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username"
        )

    if not verify_password(
        data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    payload = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(hours=10)
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role
    }


# CURRENT USER
@router.get("/me")
def me(current_user: User = Depends(get_current_user)):

    return {
        "username": current_user.username,
        "role": current_user.role
    }