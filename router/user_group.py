from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlmodel import Session, select

from model.user import User, UserGroup
from util.engine import get_session
from util.security import get_current_user

user_group_router = APIRouter()

@user_group_router.get("/user_group/")
async def get_user_groups(session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    """获取所有用户组"""
    groups = session.exec(select(UserGroup)).all()
    return groups

@user_group_router.get("/user_group/{username}")
async def get_user(username: str, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    """获取指定用户的用户组"""
    user_get = session.get(User, username)
    return user_get.groups

class CreateGroupRequest(BaseModel):
    group_name: str
    group_description: str
    can_send_message: bool

@user_group_router.post("/user_group/create")
async def create_group(request: CreateGroupRequest, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    """创建用户组"""
    existing_group = session.exec(
        select(UserGroup).where(UserGroup.group_name == request.group_name)
    ).first()
    if existing_group:
        raise HTTPException(status_code=400, detail="Group already exists")

    new_group = UserGroup(
        group_name=request.group_name,
        group_description=request.group_description,
        can_send_message=request.can_send_message
    )
    session.add(new_group)
    session.commit()
    session.refresh(new_group)

    return {"message": "User group created successfully", "group_id": new_group.group_id}

@user_group_router.delete("/user_group/{group_id}")
async def delete_group(group_id: int, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    """删除用户组"""
    group = session.get(UserGroup, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    session.delete(group)
    session.commit()

    return {"message": "User group deleted successfully"}