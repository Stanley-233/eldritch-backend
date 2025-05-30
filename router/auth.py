from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlmodel import Session, select
from util.engine import get_session
from model.user import User

class AuthRequest(BaseModel):
    username: str
    password: str

auth_router = APIRouter()

@auth_router.post("/auth/login")
async def login(request: AuthRequest, session: Session = Depends(get_session)):
    """用户登录"""
    user = session.exec(
        select(User).where(User.username == request.username)
    ).first()
    if not user:
        raise HTTPException(status_code=404, detail="No User")
    if user.password != request.password:
        raise HTTPException(status_code=403, detail="Wrong Password")
    return {"message": "Login successful"}

@auth_router.post("/auth/register")
async def register(request: AuthRequest, session: Session = Depends(get_session)):
    """用户注册"""
    existing_user = session.exec(
        select(User).where(User.username == request.username)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="用户名已存在"
        )
    new_user = User(
        username=request.username,
        password=request.password
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"message": "注册成功"}