from sqlmodel import Field, Session, SQLModel, create_engine, select

# engine.py
from sqlmodel import SQLModel, create_engine, Session
from typing import Generator

DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    """初始化数据库，创建所有表"""
    SQLModel.metadata.create_all(engine)
    print("Initialized database and created tables.")

def get_session() -> Generator[Session, None, None]:
    """获取数据库会话的依赖项"""
    with Session(engine) as session:
        yield session
