from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlmodel import Session, select
from typing import List

from util.engine import get_session
from model.user import User, UserGroup
from model.message import Message

messenger_router = APIRouter()

class MessageRequest(BaseModel):
    title: str
    content: str
    created_by: str
    access_group_ids: List[int]

@messenger_router.post("/message/create")
async def create_message(request: MessageRequest, session: Session = Depends(get_session)):
    """创建消息"""


class GetMessageRequest(BaseModel):
    username: str
@messenger_router.post("/message/get")
async def get_messages(request: GetMessageRequest, session: Session = Depends(get_session)):
    """获取用户消息"""
    user = session.exec(
        select(User).where(User.username == request.username)
    ).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Relationship 获取 Messages
    messages = []
    for group in user.groups:
        messages.extend(group.messages)
    messages = {msg.message_id: msg for msg in messages}.values()

    message_list = [
        {
            "message_id": msg.message_id,
            "title": msg.title,
            "content": msg.content,
            "created_by": msg.created_by.username if msg.created_by else None
        } for msg in messages
    ]
    return message_list
