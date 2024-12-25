"""
Author: 王猛
Date: 2024-05-10 19:14:11
LastEditors: damon wang
LastEditTime: 2024-05-15 09:39:37
FilePath: /fastapi-project/src/database.py
Description: 数据库连接相关东西

Copyright (c) 2024 by 王猛 wmdyx@outlook.com, All Rights Reserved. 
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base, DeclarativeBase
from sqlalchemy.orm.session import Session
from typing import Any, Generator

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base: DeclarativeBase = declarative_base()


def get_db() -> Generator[Session, Any, None]:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
