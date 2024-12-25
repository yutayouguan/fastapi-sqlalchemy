"""
Author: 王猛
Date: 2024-05-18 14:18:29
LastEditors: 王猛
LastEditTime: 2024-05-18 14:52:49
FilePath: /auth/database.py
Description: 

Copyright (c) 2024 by 王猛 wmdyx@outlook.com, All Rights Reserved. 
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import Any, Generator
from models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=True
)  # 创建数据库连接

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # 创建会话

Base.metadata.create_all(bind=engine)  # 创建所有表


def get_db() -> Generator[Session, Any, None]:
    """定义一个上下文管理器来获取数据库会话"""
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
