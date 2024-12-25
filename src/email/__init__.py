"""
Author: 王猛
Date: 2024-05-17 22:53:52
LastEditors: 王猛
LastEditTime: 2024-05-18 00:14:05
FilePath: /fastapi-project/src/email/__init__.py
Description: 

Copyright (c) 2024 by 王猛 wmdyx@outlook.com, All Rights Reserved. 
"""

from fastapi import APIRouter
from .router import router as email_router


router = APIRouter()

router.include_router(email_router)
