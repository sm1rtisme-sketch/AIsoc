from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from pydantic import BaseModel
from core.database import get_db
from core.config import get_config
from models.user import User

router = APIRouter()


class LoginRequest(BaseModel):
    username: str = "admin"
    password: str = ""


class UserResponse(BaseModel):
    username: str
    role: str
    is_authenticated: bool


@router.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    config = get_config()
    if config.config.auth.password and request.password != config.config.auth.password:
        raise HTTPException(status_code=401, detail="Invalid password")
    
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        user = User(username=request.username, password_hash=request.password if request.password else "admin")
        db.add(user)
        db.commit()
        db.refresh(user)
    
    return {"message": "Login successful", "user": {"username": user.username, "role": user.role}}


@router.post("/logout")
async def logout():
    return {"message": "Logout successful"}


@router.get("/me")
async def current_user():
    return {
        "username": "admin",
        "role": "default",
        "is_authenticated": True,
    }
