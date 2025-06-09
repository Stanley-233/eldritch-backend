from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from sqlmodel import Session, select
from starlette.responses import JSONResponse

from model.user import User
from util.engine import get_session
from util.security import create_token

class AuthRequest(BaseModel):
    username: str
    password: str

auth_router = APIRouter()

@auth_router.post("/auth/login")
async def login(request: AuthRequest, session: Session = Depends(get_session)):
    """用户登录"""
    user = session.get(User, request.username)
    if not user:
        raise HTTPException(status_code=404, detail="No User")
    if user.password != request.password:
        raise HTTPException(status_code=403, detail="Wrong Password")
    token = create_token(user)
    if user.is_admin:
        return JSONResponse(status_code=201, content={"message": "Admin Rights", "token": token})
    return {"message": "Login successful", "token": token}

@auth_router.post("/auth/register")
async def register(request: AuthRequest, session: Session = Depends(get_session)):
    """用户注册"""
    existing_user = session.get(User, request.username)
    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="用户名已存在"
        )
    new_user = User(
        username=request.username,
        password=request.password
    )
    # 判断表是否为空，将第一个用户设为管理员
    if not session.exec(select(User)).all():
        new_user.is_admin = True
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    token = create_token(new_user)
    if new_user.is_admin:
        return JSONResponse(status_code=201, content={"message": "Admin Rights", "token": token})
    return {"message": "Register successful", "token": token}