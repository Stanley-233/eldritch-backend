from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlmodel import Session, select
from util.engine import get_session
from model.user import User, UserGroup

users_router = APIRouter()

@users_router.get("/users/")
async def get_users(session: Session = Depends(get_session)):
    """获取所有用户"""
    users = session.exec(select(User)).all()
    return users

class GroupEditRequest(BaseModel):
    username: str
    group_id: int

@users_router.post("/users/add_group")
async def add_group(request: GroupEditRequest, session: Session = Depends(get_session)):
    """"添加用户到用户组"""
    user = session.exec(
        select(User).where(User.username == request.username)
    ).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    group = session.exec(
        select(UserGroup).where(UserGroup.group_id == request.group_id)
    ).first()
    if not group:
        raise HTTPException(status_code=406, detail="Group not found")

    if group in user.groups:
        raise HTTPException(status_code=400, detail="User already in this group")

    user.groups.append(group)
    group.users.append(user)
    session.add_all([user, group])
    session.commit()
    session.refresh(user)

    return {"message": "User added to group successfully"}

@users_router.post("/users/remove_group")
async def remove_group(request: GroupEditRequest, session: Session = Depends(get_session)):
    """从用户组中移除用户"""
    user = session.exec(
        select(User).where(User.username == request.username)
    ).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    group = session.exec(
        select(UserGroup).where(UserGroup.group_id == request.group_id)
    ).first()
    if not group:
        raise HTTPException(status_code=406, detail="Group not found")

    if group not in user.groups:
        raise HTTPException(status_code=400, detail="User not in this group")

    user.groups.remove(group)
    group.users.remove(user)
    session.add_all([group, user])
    session.commit()
    session.refresh(user)

    return {"message": "User removed from group successfully"}

