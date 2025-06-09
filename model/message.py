from sqlmodel import SQLModel, Field, Relationship
import datetime
from typing import List, Optional

class OrderGroupLink(SQLModel, table=True):
    order_id: int = Field(foreign_key="order.order_id", primary_key=True)
    group_id: int = Field(foreign_key="usergroup.group_id", primary_key=True)

# 消息-可见用户组关系
class MessageGroupLink(SQLModel, table=True):
    message_id: int = Field(foreign_key="message.message_id", primary_key=True)
    access_group_id: int = Field(foreign_key="usergroup.group_id", primary_key=True)

# 工单
class Order(SQLModel, table=True):
    order_id: int = Field(primary_key=True, index=True)
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    status: str = Field(default="open")  # 状态：open, reject, closed
    assigned_groups: List["UserGroup"] = Relationship(back_populates="orders", link_model=OrderGroupLink)
    created_at: datetime.datetime = Field(nullable=False)
    updated_at: datetime.datetime = Field(nullable=False)
    c_by_username: str = Field(foreign_key="user.username", nullable=False)
    created_by: Optional["User"] = Relationship()
    # 绑定的反馈
    report: Optional["Report"] = Relationship(back_populates="order")

# 工单反馈
class Report(SQLModel, table=True):
    report_id: int = Field(primary_key=True, index=True)
    content: str = Field(nullable=False)
    c_by_username: str = Field(foreign_key="user.username", nullable=False)
    created_by: Optional["User"] = Relationship()
    created_at: datetime.datetime = Field(nullable=False)

    order_id: int = Field(foreign_key="order.order_id", nullable=False)
    order: Optional["Order"] = Relationship(back_populates="report")

# 消息
class Message(SQLModel, table=True):
    message_id: int = Field(primary_key=True, index=True)
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    c_by_username: str = Field(foreign_key="user.username", nullable=False)
    created_by: Optional["User"] = Relationship()
    access_groups: List["UserGroup"] = Relationship(back_populates="messages", link_model=MessageGroupLink)
    created_at: datetime.datetime = Field(nullable=False)
