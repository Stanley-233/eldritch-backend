from sqlmodel import SQLModel, Field, Relationship
import datetime
from typing import List, Optional

from model.user import User, UserGroup

# 工单
class Order(SQLModel, table=True):
    order_id: int = Field(primary_key=True, index=True)
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    status: str = Field(default="open")  # 状态：open, in_progress, reject, closed
    created_by: str = Field(foreign_key="user.uid", nullable=False)
    assigned_to: str = Field(foreign_key="usergroup.group_id", nullable=True)
    created_at: datetime = Field(nullable=False)
    updated_at: datetime = Field(nullable=False)

    # 关联关系
    create_user: Optional["User"] = Relationship(back_populates="order")
    assigned_group: Optional["UserGroup"] = Relationship(back_populates="order")
    report: Optional["Report"] = Relationship(back_populates="order")

# 工单反馈
class Report(SQLModel, table=True):
    report_id: int = Field(primary_key=True, index=True)
    order_id: int = Field(foreign_key="order.order_id", nullable=False)
    content: str = Field(nullable=False)
    created_by: str = Field(foreign_key="user.uid", nullable=False)
    created_at: datetime = Field(nullable=False)

    # 绑定的工单
    order: Optional["Order"] = Relationship(back_populates="report")
    create_user: Optional["User"] = Relationship(back_populates="report")

# 消息-可见用户组关系x
class MessageAuth(SQLModel, table=True):
    message_id: int = Field(foreign_key="message.message_id", primary_key=True)
    access_group_id: int = Field(foreign_key="usergroup.group_id", primary_key=True)

# 消息
class Message(SQLModel, table=True):
    message_id: int = Field(primary_key=True, index=True)
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    created_by: str = Field(foreign_key="user.uid", nullable=False)

    crated_user: Optional["User"] = Relationship(back_populates="message")
    access_groups = Relationship(back_populates="message", link_model=MessageAuth)
