"""
Author: 王猛
Date: 2024-05-10 19:15:12
LastEditors: 王猛
LastEditTime: 2024-05-18 00:03:14
FilePath: /fastapi-project/src/main.py
Description: 

Copyright (c) 2024 by 王猛 wmdyx@outlook.com, All Rights Reserved. 
"""

from fastapi import Depends, FastAPI, HTTPException, Query, Request, Response
from sqlalchemy.orm import Session
from src.config import settings
from . import crud, models, schemas
from .database import SessionLocal, engine
from .exceptions import register_exception_handlers
from src.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from src.email import router as email_router

models.Base.metadata.create_all(bind=engine)


# 注册路由
def register_routes(app: FastAPI):
    app.include_router(auth_router, prefix="/auth", tags=["Auth模块"])
    app.include_router(email_router, prefix="/email", tags=["Email模块"])


# 注册中间件
def register_middleware(app: FastAPI):
    app.add_middleware(CORSMiddleware, **settings.cors.model_dump())


def create_app():
    app = FastAPI(**settings.app.model_dump())
    register_exception_handlers(app)
    register_routes(app)
    register_middleware(app)
    return app


app: FastAPI = create_app()
