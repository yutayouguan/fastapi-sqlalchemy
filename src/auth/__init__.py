"""
Author: 王猛
Date: 2024-05-17 22:56:14
LastEditors: 王猛
LastEditTime: 2024-05-18 00:07:31
FilePath: /fastapi-project/src/auth/__init__.py
Description: 

Copyright (c) 2024 by 王猛 wmdyx@outlook.com, All Rights Reserved. 
"""

from fastapi import APIRouter
from .router import router as user_router

router = APIRouter()

# 注册路由
router.include_router(user_router)
