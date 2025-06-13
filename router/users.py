from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlmodel import Session, select

from model.user import User, UserGroup
from util.engine import get_session
from util.security import get_current_user

users_router = APIRouter()

@users_router.get("/users/")
async def get_users(session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    """获取所有用户"""
    users = session.exec(select(User)).all()
    return [
        {"username": user.username, "is_admin": user.is_admin} for user in users
    ]

class GroupEditRequest(BaseModel):
    username: str
    group_id: int

@users_router.post("/users/add_group")
async def add_group(request: GroupEditRequest,
                    session: Session = Depends(get_session),
                    user: User = Depends(get_current_user)):
    """"添加用户到用户组"""
    user_modify = session.get(User, request.username)
    group = session.get(UserGroup, request.group_id)
    if not group:
        raise HTTPException(status_code=406, detail="Group not found")

    if group in user_modify.groups:
        raise HTTPException(status_code=400, detail="User already in this group")

    user_modify.groups.append(group)
    session.add_all([user_modify, group])
    session.commit()
    session.refresh(user_modify)

    return {"message": "User added to group successfully"}

@users_router.post("/users/remove_group")
async def remove_group(request: GroupEditRequest,
                       session: Session = Depends(get_session),
                       user: User = Depends(get_current_user)):
    """从用户组中移除用户"""
    user_modify = session.get(User, request.username)
    group = session.get(UserGroup, request.group_id)
    if not group:
        raise HTTPException(status_code=406, detail="Group not found")

    if group not in user_modify.groups:
        raise HTTPException(status_code=400, detail="User not in this group")

    user_modify.groups.remove(group)
    session.add_all([group, user_modify])
    session.commit()
    session.refresh(user_modify)

    return {"message": "User removed from group successfully"}

