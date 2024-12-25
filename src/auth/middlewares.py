"""
Author: 王猛
Date: 2024-05-11 03:08:07
LastEditors: 王猛
LastEditTime: 2024-05-11 10:08:11
FilePath: /fastapi-project/src/auth/middlewares.py
Description: 用于处理请求前后的逻辑，如身份验证、日志记录等

Copyright (c) 2024 by 王猛 wmdyx@outlook.com, All Rights Reserved. 
"""

from fastapi import Request, Header, Response


async def authenticate_request(request: Request, auth_header: str = Header(...)):
    # 实现身份验证逻辑
    ...


async def log_request(request: Request, response: Response):
    # 实现日志记录逻辑
    ...


async def add_cors_headers(request: Request, call_next):
    # 实现跨域资源共享逻辑
    ...


async def add_security_headers(request: Request, call_next):
    # 实现安全头逻辑
    ...


async def add_custom_headers(request: Request, call_next):
    # 实现自定义头逻辑
    ...


async def add_custom_response_headers(request: Request, call_next):
    # 实现自定义响应头逻辑
    ...


async def add_process_time_header(request: Request, call_next):
    # 实现处理时间头逻辑
    import time

    start_time = time.time()
    response: Response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
