from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

from model.message import Message, MessageAuth

class UserGroupLink(SQLModel, table=True):
    user_id: str = Field(foreign_key="user.username", primary_key=True)
    group_id: int = Field(foreign_key="usergroup.group_id", primary_key=True)

class User(SQLModel, table=True):
    username: str = Field(primary_key=True, index=True)
    password: str = None
    groups: List["UserGroup"] = Relationship(back_populates="users", link_model=UserGroupLink)

class UserGroup(SQLModel, table=True):
    group_id: int = Field(primary_key=True, index=True)
    group_name: str = None
    group_description: str = None

    users: List["User"] = Relationship(back_populates="groups", link_model=UserGroupLink)
    messages: List["Message"] = Relationship(back_populates="groups", link_model=MessageAuth)