"""
Author: 王猛
Date: 2024-05-11 10:12:17
LastEditors: damon wang
LastEditTime: 2024-05-15 09:34:47
FilePath: /fastapi-project/src/middlewares.py
Description: 全局中间件

Copyright (c) 2024 by 王猛 wmdyx@outlook.com, All Rights Reserved. 
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings


async def init_middleware(app: FastAPI):
    # 跨域中间件
    app.add_middleware(CORSMiddleware, **settings.cors.model_dump())

    app.user_middleware
