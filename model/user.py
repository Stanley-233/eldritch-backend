from typing import List

from sqlmodel import SQLModel, Field, Relationship

from model.message import MessageGroupLink, OrderGroupLink


class UserGroupLink(SQLModel, table=True):
    username: str = Field(foreign_key="user.username", primary_key=True)
    group_id: int = Field(foreign_key="usergroup.group_id", primary_key=True)

class User(SQLModel, table=True):
    username: str = Field(primary_key=True, index=True)
    password: str = None
    is_admin: bool = False
    groups: List["UserGroup"] = Relationship(back_populates="users", link_model=UserGroupLink)

class UserGroup(SQLModel, table=True):
    group_id: int = Field(primary_key=True, index=True)
    group_name: str = None
    group_description: str = None
    can_send_message: bool = False

    users: List["User"] = Relationship(back_populates="groups", link_model=UserGroupLink)
    messages: List["Message"] = Relationship(back_populates="access_groups", link_model=MessageGroupLink)
    orders: List["Order"] = Relationship(back_populates="assigned_groups", link_model=OrderGroupLink)
