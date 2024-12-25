"""
Author: 王猛
Date: 2024-05-12 20:10:04
LastEditors: 王猛
LastEditTime: 2024-05-12 23:34:28
FilePath: /fastapi-project/src/schemas.py
Description:  Pydantic 模型 (数据验证效验)

Copyright (c) 2024 by 王猛 wmdyx@outlook.com, All Rights Reserved. 
"""

from pydantic import BaseModel, ConfigDict


class ItemBase(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    owner_id: int


class UserBase(BaseModel):
    username: str
    full_name: str | None = None
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    is_active: bool
    items: list[Item] = []
