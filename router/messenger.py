import datetime
from typing import List

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlmodel import Session, select

from model.message import Message
from model.user import User, UserGroup
from util.engine import get_session

messenger_router = APIRouter()

class MessageRequest(BaseModel):
    title: str
    content: str
    created_by: str
    access_group_ids: List[int]

@messenger_router.post("/message/create")
async def create_message(request: MessageRequest, session: Session = Depends(get_session)):
    """创建消息"""
    user = session.get(User, request.created_by)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not any(group.can_send_message for group in user.groups):
        raise HTTPException(status_code=403, detail="User does not have permission to send messages")

    # 验证Access Groups是否正确
    access_groups = []
    for group_id in request.access_group_ids:
        group = session.get(UserGroup, group_id)
        if not group:
            raise HTTPException(status_code=404, detail=f"No such group with id {group_id} found")
        access_groups.append(group)

    new_message = Message(
        title=request.title,
        content=request.content,
        created_by=user,
        access_groups=access_groups,
        created_at=datetime.datetime.now()
    )
    session.add(new_message)
    session.commit()
    session.refresh(new_message)

    return {"message": "Message created successfully", "message_id": new_message.message_id}


class GetMessageRequest(BaseModel):
    username: str
@messenger_router.post("/message/get")
async def get_messages(request: GetMessageRequest, session: Session = Depends(get_session)):
    """获取用户消息"""
    user = session.get(User, request.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.groups:
        raise HTTPException(status_code=403, detail="User does not belong to any groups")

    # Relationship 获取 Messages
    messages = []
    for group in user.groups:
        messages.extend(group.messages)
    messages = {msg.message_id: msg for msg in messages}.values()
    create_messages = session.exec(
        select(Message).where(Message.created_by == user)
    ).all()
    messages = list(messages) + create_messages
    # 去重
    messages = list({msg.message_id: msg for msg in messages}.values())

    message_list = [
        {
            "message_id": msg.message_id,
            "title": msg.title,
            "content": msg.content,
            "created_by": msg.created_by.username if msg.created_by else None,
            "created_at": msg.created_at if msg.created_by else None,
        } for msg in messages
    ]
    return message_list
