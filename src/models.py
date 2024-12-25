"""
Author: 王猛
Date: 2024-05-10 19:12:44
LastEditors: damon wang
LastEditTime: 2024-05-15 09:33:37
FilePath: /fastapi-project/src/models.py
Description: 全局模型

Copyright (c) 2024 by 王猛 wmdyx@outlook.com, All Rights Reserved. 
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):  # type: ignore
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    items = relationship("Item", back_populates="owner")

    def __repr__(self):
        return f"<User(email='{self.email}')>"


class Item(Base):  # type: ignore
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")

    def __repr__(self):
        return f"<Item(title='{self.title}')>"
